from django.urls import path
from app.views.main import *

urlpatterns = [
    path("", homepage, name="homepage"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("signup/", signup, name="signup"),
    path("products/", product_list, name="product_list"),
    path("403/", forbidden, name="forbidden"),
    path("404/", notfound, name="not_found"),
]