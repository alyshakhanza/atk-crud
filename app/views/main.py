from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.models.user import UserAccount
from app.models.customer import Customer, CustomerProfile

def homepage(request) : 
    context = {}
    if request.user.is_authenticated and request.user.type == UserAccount.Types.CUSTOMER:
        profile, created = CustomerProfile.objects.get_or_create(
            customer=request.user
        )
        context["profile"] = profile

    return render(request, "app/public/homepage.html", context)

def logout_view(request):
    logout(request)
    return redirect("login")

def login_view(request):
    if request.user.is_authenticated:
        if request.user.type == UserAccount.Types.CUSTOMER:
            return redirect("homepage")
        elif request.user.type == UserAccount.Types.ADMIN:
            return redirect("dashboard")
        
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.type == UserAccount.Types.ADMIN:
                return redirect("dashboard")
            else:
                return redirect("homepage")
        else:
            messages.error(request, "Email atau password salah.")

    return render(request, "app/public/login.html")

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Validasi sederhana
        if not all([email, password, name, gender, phone, address]):
            messages.error(request, "Semua field harus diisi.")
            return render(request, "app/public/signup.html")

        try:
            user = Customer.objects.create_user(email=email, password=password)
            CustomerProfile.objects.create(
                customer=user,
                name=name,
                gender=gender,
                phone=phone,
                address=address
            )

            login(request, user)
            return redirect("homepage")

        except Exception as e:
            messages.error(request, f"Signup failed: {e}")

    return render(request, "app/public/signup.html")

def forbidden(request):
    return render(request, "app/public/403.html")

def notfound(request):
    return render(request, "app/public/404.html")