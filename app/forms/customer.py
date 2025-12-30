from django import forms
from app.models.customer import *
from app.models.cart import *
from app.models.product import Item
from app.models.order import *

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['name', 'gender', 'phone', 'address', 'image']

    def clean_customer(self):
        customer = self.cleaned_data.get("customer")
        if CustomerProfile.objects.filter(customer=customer).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Customer Profile with this name already exists")
        return customer
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone.isdigit():
            raise forms.ValidationError("Phone must contain only digits.")
        if len(phone) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits long.")
        return phone
    
class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')], required=True)
    total_amount = forms.DecimalField(max_digits=10, decimal_places=0, required=True)
    card_number = forms.CharField(max_length=16, required=False)
    card_expiry = forms.CharField(max_length=5, required=False)  
    card_cvc = forms.CharField(max_length=3, required=False)

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        if card_number and len(card_number) != 16:
            raise forms.ValidationError("Card number must be 16 digits long.")
        return card_number
    
# class CartItemForm(forms.ModelForm):
#     class Meta:
#         model = CartItem
#         fields = ['quantity']

#     def clean_quantity(self):
#         qty = self.cleaned_data.get('quantity')
#         if qty < 1:
#             raise forms.ValidationError("Quantity must be at least 1.")
#         if self.instance.item.stock < qty:
#             raise forms.ValidationError(f"Only {self.instance.item.stock} items available in stock.")
#         return qty
    
#     def clean_item(self):
#         item = self.cleaned_data.get("item")
#         cart = getattr(self.instance, 'cart', None)

#         if cart and CartItem.objects.filter(cart=cart, item=item).exclude(pk=self.instance.pk).exists():
#             raise forms.ValidationError("This item is already in the cart.")
#         return item

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.item_obj = kwargs.pop('item_obj', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity', 1)
        if qty is None: 
            qty = 1
        
        if self.item_obj and qty > self.item_obj.stock:
            raise forms.ValidationError(f"Stok tidak cukup. Hanya tersisa {self.item_obj.stock}.")
        return qty

    def save(self):
        qty = self.cleaned_data.get('quantity')
        cart, _ = Cart.objects.get_or_create(user=self.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=self.item_obj)

        if not created:
            cart_item.quantity += qty
        else:
            cart_item.quantity = qty
            
        cart_item.save()
        return cart_item
class OrderFilterForm(forms.Form):
    order_status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Order.STATUS_CHOICES),
        required=False
    )
    start_date = forms.DateField(required=False, widget=forms.SelectDateWidget)
    end_date = forms.DateField(required=False, widget=forms.SelectDateWidget)

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'price']

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        item = self.cleaned_data.get('item')
        if qty is None:
            raise forms.ValidationError("Quantity is required.")
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        if item and qty > item.stock:
            raise forms.ValidationError(f"Quantity cannot exceed available stock ({item.stock}).")
        return qty
    
    def clean_price(self):
        total = self.cleaned_data.get('price')
        if total is None:
            raise forms.ValidationError("Price is required.")
        if total <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return total