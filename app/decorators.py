from django.shortcuts import redirect
from functools import wraps
from app.models.user import UserAccount

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            if request.user.type != required_role:
                if request.user.type == UserAccount.Types.CUSTOMER:
                    return redirect("forbidden")
                elif request.user.type == UserAccount.Types.ADMIN:
                    return redirect("forbidden")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
