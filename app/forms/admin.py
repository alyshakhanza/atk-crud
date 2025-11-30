from django import forms
from app.models.product import *
from app.models.order import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Category.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Category with this name already exists")
        return name

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Brand.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Brand with this name already exists")
        return name
    
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'brand', 'description', 'color', 'price', 'stock', 'size', 'image']

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Item.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Item with this name already exists")
        return name
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock
    
class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']