from django.urls import path
from app.views.customer import *

urlpatterns = [
    path("payment/", payment, name="payment"),
    path("payment/success/", payment_success, name="payment_success"),
    path("cart/", cart, name="cart"),
    path("profile/", profile, name="profile"),
    path("orders/", all_orders, name="customer_orders"),
]
