from django.shortcuts import redirect
from django.contrib import messages
from app.models.user import UserAccount

class AdminRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path  
        if path.startswith("/admin/"):

            if not request.user.is_authenticated:
                return redirect("login")
            if request.user.type != UserAccount.Types.ADMIN:
                return redirect("forbidden")

        return self.get_response(request)

class CustomerRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith("/admin/") or path.startswith("/login") or path.startswith("/static/"):
            return self.get_response(request)
        user = getattr(request, "user", None)

        if not request.user.is_authenticated:
            messages.error(request, "Please login first.")
            return redirect("login")

        if getattr(user, "type", None) != UserAccount.Types.CUSTOMER:
            messages.error(request, "Access denied!")
            return redirect("homepage") 

        return self.get_response(request)