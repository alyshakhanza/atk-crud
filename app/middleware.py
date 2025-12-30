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

        # Public paths (do not restrict)
        PUBLIC_PATHS = (
            "/login",
            "/logout",
            "/signup",
            "/static/",
            "/admin/",
            "/"  # Admin has its own middleware
        )

        protected_paths = ['/u/cart', '/u/orders']

        if path in protected_paths and not request.user.is_authenticated:
            return redirect('login')

        # If path starts with a public path, skip middleware
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return self.get_response(request)

        user = getattr(request, "user", None)

        # Require login
        if not request.user.is_authenticated:
            messages.error(request, "Please login first.")
            return redirect("login")

        # Require customer type
        if getattr(user, "type", None) != UserAccount.Types.CUSTOMER:
            messages.error(request, "Access denied!")
            return redirect("homepage")

        return self.get_response(request)
    def __init__(self, get_response):
        self.get_response = get_response
