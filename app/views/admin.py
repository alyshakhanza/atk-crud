from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from datetime import timedelta
from xhtml2pdf import pisa
from app.models.user import UserAccount
from django.db.models import Sum
from app.models.product import *
from app.models.order import Order
from app.forms.admin import *
# from app.forms.customer import OrderForm

def dashboard(request):
    # --- Statistik Global ---
    total_orders = Order.objects.count()
    revenue_data = Order.objects.exclude(status='cancelled').aggregate(total=Sum('total_price'))
    total_revenue = revenue_data['total'] if revenue_data['total'] else 0
    total_products = Item.objects.count()
    
    # --- Top Product (Data Cards Atas) ---
    top_product_data = OrderItem.objects.values('item__name') \
        .annotate(total_sold=Sum('quantity')).order_by('-total_sold').first()
    top_product_name = top_product_data['item__name'] if top_product_data else "-"
    top_product_sold = top_product_data['total_sold'] if top_product_data else 0

    # --- Recent Orders (Tabel Kiri) ---
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    # --- LOGIC BARU: Weekly Sales Chart (Grafik Batang) ---
    today = timezone.now().date()
    weekly_sales = []
    max_daily_orders = 1 # Default 1 agar tidak divide by zero jika kosong

    for i in range(6, -1, -1): # Loop 7 hari ke belakang (H-6 sampai H-0)
        date_obj = today - timedelta(days=i)
        # Hitung jumlah order per hari (exclude cancelled)
        count = Order.objects.filter(created_at__date=date_obj).exclude(status='cancelled').count()
        
        if count > max_daily_orders:
            max_daily_orders = count
            
        weekly_sales.append({
            'day_label': date_obj.strftime('%a')[0], # Ambil huruf pertama hari (S, M, T...)
            'count': count,
            'is_today': (date_obj == today)
        })

    # --- LOGIC BARU: Top Category Gauge ---
    top_category_data = OrderItem.objects.values('item__category__name') \
        .annotate(total_qty=Sum('quantity')).order_by('-total_qty').first()
    
    if top_category_data:
        top_cat_name = top_category_data['item__category__name']
        top_cat_qty = top_category_data['total_qty']
        
        # Hitung persentase dominasi kategori ini terhadap total seluruh item terjual
        total_items_sold = OrderItem.objects.aggregate(total=Sum('quantity'))['total'] or 1
        top_cat_percentage = int((top_cat_qty / total_items_sold) * 100)
    else:
        top_cat_name = "No Data"
        top_cat_qty = 0
        top_cat_percentage = 0

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_products": total_products,
        "top_product_name": top_product_name,
        "top_product_sold": top_product_sold,
        "recent_orders": recent_orders,
        
        # Data untuk Grafik Kanan
        "weekly_sales": weekly_sales,
        "max_daily_orders": max_daily_orders,
        "top_cat_name": top_cat_name,
        "top_cat_qty": top_cat_qty,
        "top_cat_percentage": top_cat_percentage,
    }

    return render(request, "app/admin/dashboard.html", context)
# =======================
# ITEMS
# templates/app/admin/items/...
# =======================
def item_list(request):
    items = Item.objects.select_related('category', 'brand').all().order_by('-id')
    return render(request, "app/admin/items/list.html", {"items": items})

def download_item_pdf(request):
    # 1. Ambil data
    items = Item.objects.all().order_by('category', 'name')
    
    # 2. Render template HTML khusus untuk PDF
    template_path = 'app/admin/items/pdf_template.html'
    context = {'items': items}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products_report.pdf"'
    
    # 3. Konversi HTML ke PDF
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(
        html, dest=response
    )
    
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

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
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return redirect("item_list")

    if request.method == "POST":
        item.name = request.POST.get("name")
        item.category_id = request.POST.get("category")
        item.brand_id = request.POST.get("brand")
        item.description = request.POST.get("description")
        item.color = request.POST.get("color")
        item.price = request.POST.get("price")
        item.stock = request.POST.get("stock")
        item.size = request.POST.get("size")
        
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.save()
        return redirect("item_list")

    categories = Category.objects.all()
    brands = Brand.objects.all()

    return render(request, "app/admin/items/edit.html", {
        "item": item,
        "categories": categories,
        "brands": brands,
    })

def item_delete(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
        if request.method == "POST":
            if item.image:
                item.image.delete(save=False)
                
            item.delete()
            
    except Item.DoesNotExist:
        pass 
    return redirect("item_list")
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

def category_delete(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        if request.method == "POST":
            category.delete()
            
    except Category.DoesNotExist:
        pass 
    return redirect("category_list")
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

def brand_delete(request, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        if request.method == "POST":
            brand.delete()
            
    except Brand.DoesNotExist:
        pass 
    return redirect("brand_list")
# =======================
# ORDERS
# templates/app/admin/orders/all_orders.html
# =======================
def orders(request):
    orders_list = Order.objects.all().order_by('-created_at')

    stats = Order.objects.aggregate(
        total=Count('id'),
        pending=Count('id', filter=Q(status='pending')),
        delivery=Count('id', filter=Q(status='packed')), 
        cancelled=Count('id', filter=Q(status='cancelled')),
    )

    context = {
        "orders": orders_list,
        "total_orders": stats['total'],
        "pending_orders": stats['pending'],
        "delivery_orders": stats['delivery'],
        "cancelled_orders": stats['cancelled'],
    }

    return render(request, "app/admin/order/list.html", context)

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
