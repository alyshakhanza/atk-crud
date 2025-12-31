from django.urls import path
from app.views.customer import *

urlpatterns = [
    path("cart/", cart, name="cart"),
    path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", update_cart, name="update_cart"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout, name="checkout"),
    path("payment/success/<int:order_id>/", payment_success, name="payment_success"),
    path("invoice/<int:order_id>/", export_invoice, name="export_invoice"),
    
    path("product/<int:item_id>/", product_detail, name="product_detail"),
    path("profile/", profile, name="profile"),
    path("orders/", all_orders, name="customer_orders"),
]
