from django.urls import path
from app.views.admin import *


urlpatterns = [
    path("", dashboard, name="dashboard"),

    # Category
    path("category/", category_list, name="category_list"),
    path("category/add/", category_create, name="category_create"),
    path("category/<int:category_id>/edit/", category_edit, name="category_edit"),
    path('category/delete/<int:category_id>/', category_delete, name='category_delete'),

    # Brand
    path("brand/", brand_list, name="brand_list"),
    path("brand/add/", brand_create, name="brand_create"),
    path("brand/<int:brand_id>/edit/", brand_edit, name="brand_edit"),
    path('brand/delete/<int:brand_id>/', brand_delete, name='brand_delete'),

    # Items
    path("items/", item_list, name="item_list"),
    path("items/add/", item_create, name="item_create"),
    path("items/<int:item_id>/edit/", item_edit, name="item_edit"),
    path('items/delete/<int:item_id>/', item_delete, name='item_delete'),
    path('items/pdf/', download_item_pdf, name='item_pdf'),

    # Orders
    path("orders/", orders, name="orders"),
    path("orders/<int:order_id>/edit/", order_edit, name="order_edit"),
]