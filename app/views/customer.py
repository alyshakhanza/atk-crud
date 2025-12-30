from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models.user import UserAccount
from django.db.models import Q
from app.models.product import Item, Category, Brand
from app.models.customer import CustomerProfile, Customer
from app.models.order import Order, OrderItem, Payment
from app.models.cart import *
from django.http import HttpResponseRedirect
from app.forms.customer import OrderFilterForm, OrderItemForm, CustomerProfileForm, AddToCartForm, PaymentForm

def profile(request):
    user = request.user
    profile, created = CustomerProfile.objects.get_or_create(customer=user)

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")  
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, "app/customer/profile.html", {
        "form": form,
        "profile": profile
    })

def payment(request):
    return render(request, "app/customer/payment.html")

def payment_success(request):
    return render(request, "app/customer/payment_success.html")

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related('item').all()
    cart_total = sum(item.quantity * item.item.price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        # 'grand_total': grand_total,
    }
    
    return render(request, 'app/customer/cart.html', context)

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        action = request.POST.get('action')
        
        if action == 'increase':
            if cart_item.quantity < cart_item.item.stock:
                cart_item.quantity += 1
                cart_item.save()
            else:
                messages.warning(request, f"Stok hanya tersedia {cart_item.item.stock}.")
                
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                
    return redirect('cart')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, "Item berhasil dihapus dari keranjang.")
        
    return redirect('cart')

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST': 
        form = AddToCartForm(request.POST or {'quantity': 1}, user=request.user, item_obj=item)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"{item.name} berhasil ditambahkan ke keranjang.")
        else:
            error_msg = form.errors.get('quantity', ['Gagal menambahkan item.'])[0]
            messages.error(request, error_msg)

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'product_list'
    return redirect(next_url)

def all_orders(request):
    user = request.user
    customer_profile = user.profile
    orders = Order.objects.filter(customer=customer_profile)
    form = OrderFilterForm(request.GET)

    if form.is_valid():
        order_status = form.cleaned_data.get("order_status")
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")

        if order_status:
            orders = orders.filter(status=order_status)

        if start_date:
            orders = orders.filter(order_date__gte=start_date)

        if end_date:
            orders = orders.filter(order_date__lte=end_date)

    return render(request, "app/customer/orders.html", {
        "orders": orders,
        "form": form,
    })

def order_create(request):
    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            status="pending",
            total_price=0 
        )

        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()

            # update total price
            order.total_price = sum(item.quantity * item.price for item in order.items.all())
            order.save()

            return redirect("payment")
        else:
            order.delete() 
    else:
        form = OrderItemForm()

    return render(request, "app/order/create.html", {"form": form})

def product_list(request):
    items = Item.objects.all().order_by('-created_at')
    search_query = request.GET.get('q')
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    category_id = request.GET.get('category')
    if category_id:
        items = items.filter(category_id=category_id)

    # 4. Filter Brand
    brand_id = request.GET.get('brand')
    if brand_id:
        items = items.filter(brand_id=brand_id)

    # 5. Data untuk Sidebar
    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        "items": items,
        "categories": categories,
        "brands": brands,
        "active_category": int(category_id) if category_id else None,
        "active_brand": int(brand_id) if brand_id else None,
        "search_query": search_query
    }

    return render(request, "app/public/product_list.html", context)

def product_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    related_items = Item.objects.filter(category=item.category).exclude(id=item.id)[:4]

    context = {
        "item": item,
        "related_items": related_items,
    }
    return render(request, "app/customer/product_detail.html", context)

def checkout(request):
    # Ambil cart user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('item').all()

    # Jika keranjang kosong, lempar balik
    if not cart_items:
        messages.warning(request, "Keranjang Anda kosong.")
        return redirect('product_list')

    # Hitung Subtotal saja
    subtotal = sum(item.quantity * item.item.price for item in cart_items)

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        
        # Validasi sederhana
        if not address or not payment_method:
            messages.error(request, "Mohon lengkapi alamat dan metode pembayaran.")
            return redirect('checkout')

        try:
            with transaction.atomic():
                # 1. Buat Order Baru
                order = Order.objects.create(
                    user=request.user,
                    total_price=subtotal,
                    status='pending' # Default status
                )

                # 2. Pindahkan item dari Cart ke OrderItem
                for c_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        item=c_item.item,
                        quantity=c_item.quantity,
                        price=c_item.item.price # Simpan harga saat checkout (snapshot)
                    )

                # 3. Simpan Data Pembayaran
                Payment.objects.create(
                    order=order,
                    amount=subtotal,
                    method=payment_method,
                    success=True # Anggap auto-success untuk simulasi
                )

                # 4. Kosongkan Keranjang
                cart.items.all().delete()

                messages.success(request, "Pesanan berhasil dibuat!")
                return redirect('customer_orders') # Redirect ke halaman list order

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan: {e}")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }
    return render(request, 'app/customer/checkout.html', context)