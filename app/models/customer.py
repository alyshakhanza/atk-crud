from django.db import models
from .user import UserAccount

class CustomerManager(models.Manager):
    def create_user(self , email , password = None):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        email  = email.lower()
        user = self.model(
            email = email
        )
        user.set_password(password)
        user.type = UserAccount.Types.CUSTOMER
        user.is_customer = True
        user.save(using = self._db)
        return user
    
    def get_queryset(self , *args,  **kwargs):
        queryset = super().get_queryset(*args , **kwargs)
        queryset = queryset.filter(type = UserAccount.Types.CUSTOMER)
        return queryset    

class Customer(UserAccount):
    class Meta : 
        proxy = True
    objects = CustomerManager()
    
    def save(self , *args , **kwargs):
        if not self.id or self.id == None : 
            self.type = UserAccount.Types.CUSTOMER
        return super().save(*args , **kwargs)
    
class CustomerProfile(models.Model):
    customer = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='custpic/', blank=True, null=True)

    
    def __str__(self):
        return f"{self.customer.email} Profile"
