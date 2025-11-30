from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models.user import UserAccount
from app.models.customer import CustomerProfile, Customer
from app.models.order import Order, OrderItem
from app.models.cart import *
from app.forms.customer import OrderFilterForm, OrderItemForm, CustomerProfileForm, CartItemForm

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
    items = cart.items.all() 

    if request.method == "POST":
        for cart_item in items:
            qty = request.POST.get(f"quantity_{cart_item.id}")
            if qty:
                try:
                    qty = int(qty)
                    if qty < 1:
                        cart_item.delete()  
                    else:
                        cart_item.quantity = qty
                        cart_item.save()
                except ValueError:
                    messages.error(request, f"Invalid quantity for {cart_item.item.name}")

            if f"delete_{cart_item.id}" in request.POST:
                cart_item.delete()
                messages.success(request, f"Removed {cart_item.item.name} from cart.")

        return redirect("cart") 
    
    subtotal_list = [(item, item.quantity * item.item.price) for item in items]
    total = sum(subtotal for _, subtotal in subtotal_list)

    return render(request, "app/customer/cart.html", {
        "cart": cart,
        "items": items,
        "subtotal_list": subtotal_list,
        "total": total
    })

def add_to_cart(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.filter(cart=cart, item=item).first()

    if request.method == "POST":
        if cart_item:
            form = CartItemForm(request.POST, instance=cart_item)
        else:
            form = CartItemForm(request.POST)

        if form.is_valid():
            new_cart_item = form.save(commit=False)
            new_cart_item.cart = cart
            new_cart_item.item = item
            new_cart_item.save()
            messages.success(request, f"{item.name} added to cart successfully!")
            return redirect("cart") 
        else:
            messages.error(request, "Failed to add item to cart. Please fix the errors below.")
    else:
        form = CartItemForm(instance=cart_item)

    return render(request, "app/customer/cart_add.html", {
        "form": form,
        "item": item,
    })

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