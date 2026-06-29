from django import forms
from .models import Order


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Shipping Address')
    note = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}), label='Order Note (optional)')


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
