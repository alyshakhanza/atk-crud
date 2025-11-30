from django.shortcuts import render, redirect
from app.models.user import UserAccount
from app.models.product import *
from app.models.order import Order
from app.forms.admin import *
# from app.forms.customer import OrderForm

def dashboard(request):
    return render(request, "app/admin/dashboard.html")

# =======================
# ITEMS
# templates/app/admin/items/...
# =======================
def item_list(request):
    items = Item.objects.all().order_by('-id')
    return render(request, "app/admin/items/list.html", {"items": items})

def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("item_list")
        else:
            return render(request, "app/admin/items/create.html", {"form": form})

    form = ItemForm()
    return render(request, "app/admin/items/create.html", {"form": form})

def item_edit(request, item_id):
    item = Item.objects.get(id=item_id)

    if request.method == "POST":
        item.name = request.POST.get("name")
        item.category_id = request.POST.get("category")
        item.brand_id = request.POST.get("brand")
        item.description = request.POST.get("description")
        item.color = request.POST.get("color")
        item.price = request.POST.get("price")
        item.stock = request.POST.get("stock")
        item.size = request.POST.get("size")
        item.image = request.POST.get("image")
        item.save()

        return redirect("item_list")

    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(request, "app/admin/items/edit.html", {
        "item": item,
        "categories": categories,
        "brands": brands,
    })

# =======================
# CATEGORY
# templates/app/admin/category/...
# =======================
def category_list(request):
    categories = Category.objects.all().order_by('-id')
    return render(request, "app/admin/category/list.html", {"categories": categories})

def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("category_list")
        else:
            return render(request, "app/admin/category/create.html", {"form": form})

    form = CategoryForm()
    return render(request, "app/admin/category/create.html", {"form": form})

def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
        else:
            return render(request, "app/admin/category/edit.html", {"form": form, "category": category})

    form = CategoryForm(instance=category)
    return render(request, "app/admin/category/edit.html", {"form": form, "category": category})
# =======================
# BRAND
# templates/app/admin/brand/...
# =======================
def brand_list(request):
    brands = Brand.objects.all().order_by('-id')
    return render(request, "app/admin/brand/list.html", {"brands": brands})

def brand_create(request):
    if request.method == "POST":
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("brand_list")
        else:
            return render(request, "app/admin/brand/create.html", {"form": form})

    form = BrandForm()
    return render(request, "app/admin/brand/create.html", {"form": form})

def brand_edit(request, brand_id):
    brand = Brand.objects.get(id=brand_id)

    if request.method == "POST":
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect("brand_list")
        else:
            return render(request, "app/admin/brand/edit.html", {"form": form, "brand": brand})

    form = BrandForm(instance=brand)
    return render(request, "app/admin/brand/edit.html", {"form": form, "brand": brand})

# =======================
# ORDERS
# templates/app/admin/orders/all_orders.html
# =======================
def orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "app/admin/order/list.html", {"orders": orders})

def order_edit(request, order_id):
    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        form = AdminOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("orders") 
        else:
            return render(request, "app/admin/order/edit.html", {
                "form": form,
                "order": order
            })

    form = AdminOrderForm(instance=order)
    return render(request, "app/admin/order/edit.html", {
        "form": form,
        "order": order
    })
