from django.db import models
from .user import UserAccount
from .product import Item

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Unpaid'),
        ('packed', 'Packed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('return', 'Return'),
    )
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order {self.order.id}"
    

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=50, choices=(('credit_card','Credit Card'), ('bank_transfer','Bank Transfer')))
    paid_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {'Success' if self.success else 'Pending'}"
