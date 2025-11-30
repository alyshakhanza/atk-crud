from django.urls import path
from app.views.admin import *


urlpatterns = [
    path("", dashboard, name="dashboard"),

    # Category
    path("category/", category_list, name="category_list"),
    path("category/add/", category_create, name="category_create"),
    path("category/<int:pk>/edit/", category_edit, name="category_edit"),

    # Brand
    path("brand/", brand_list, name="brand_list"),
    path("brand/add/", brand_create, name="brand_create"),
    path("brand/<int:pk>/edit/", brand_edit, name="brand_edit"),

    # Items
    path("items/", item_list, name="item_list"),
    path("items/add/", item_create, name="item_create"),
    path("items/<int:pk>/edit/", item_edit, name="item_edit"),

    # Orders
    path("orders/", orders, name="orders"),
]