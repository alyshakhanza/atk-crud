from app.models.customer import CustomerProfile

def profile_processor(request):
    profile = None
    if request.user.is_authenticated:
        profile, _ = CustomerProfile.objects.get_or_create(customer=request.user)
    return {"profile": profile}