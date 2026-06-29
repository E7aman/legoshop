from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from legoshop.catalog.models import Product
from .cart import Cart
from .forms import AddToCartForm


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_form'] = AddToCartForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        qty = form.cleaned_data['quantity']
        override = form.cleaned_data['override']
        cart.add(product, quantity=qty, override_quantity=override)
        messages.success(request, f'"{product.name}" added to cart.')
    return redirect('cart:detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'"{product.name}" removed from cart.')
    return redirect('cart:detail')
