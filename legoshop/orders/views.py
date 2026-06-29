from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from legoshop.cart.cart import Cart
from legoshop.accounts.views import admin_required
from .models import Order, OrderItem
from .forms import CheckoutForm, OrderStatusForm


@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                note=form.cleaned_data.get('note', ''),
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity'],
                )
            order.calculate_total()
            cart.clear()
            messages.success(request, f'Order #{order.pk} placed successfully!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        # Pre-fill address from profile
        initial = {}
        if request.user.address:
            initial['shipping_address'] = request.user.address
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Clients can only see their own orders
    if not request.user.is_shop_admin() and order.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('catalog:index')
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


# ─── Admin order management ───────────────────────────────────────────────────

@login_required
@admin_required
def admin_order_list(request):
    orders = Order.objects.all().select_related('user')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    return render(request, 'orders/admin_order_list.html', {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'current_status': status_filter,
    })


@login_required
@admin_required
def admin_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f'Order #{order.pk} status updated to "{order.get_status_display()}".')
            return redirect('orders:admin_order_detail', pk=order.pk)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'orders/admin_order_detail.html', {'order': order, 'form': form})
