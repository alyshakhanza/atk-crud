from django.urls import path
from app.views.customer import *

urlpatterns = [
    path("payment/", payment, name="payment"),
    path("payment/success/", payment_success, name="payment_success"),
    path("checkout/", checkout, name="checkout"),
    
    path("cart/", cart, name="cart"),
    path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    
    path("product/<int:item_id>/", product_detail, name="product_detail"),
    path("profile/", profile, name="profile"),
    path("orders/", all_orders, name="customer_orders"),
]
