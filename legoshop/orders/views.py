import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from legoshop.cart.cart import Cart
from legoshop.accounts.views import admin_required
from .models import Order, OrderItem
from .forms import CheckoutForm, OrderStatusForm

stripe.api_key = settings.STRIPE_SECRET_KEY


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

            # Создаём PaymentIntent на сумму заказа.
            # Stripe считает суммы в минимальных единицах валюты (центы для USD),
            # поэтому умножаем на 100.
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),
                currency='usd',
                metadata={'order_id': order.id},
                automatic_payment_methods={'enabled': True},
            )
            order.stripe_payment_intent_id = intent.id
            order.save(update_fields=['stripe_payment_intent_id'])

            # client_secret нужен фронтенду, чтобы Stripe.js знал,
            # какой именно платёж подтверждать. Кладём в сессию —
            # так он не потеряется, если пользователь перезагрузит страницу оплаты.
            request.session[f'order_{order.id}_client_secret'] = intent.client_secret

            # ВАЖНО: корзину пока НЕ очищаем и заказ пока НЕ считаем оформленным —
            # это произойдёт только после реального подтверждения оплаты.
            return redirect('orders:payment', pk=order.pk)
    else:
        initial = {}
        if request.user.address:
            initial['shipping_address'] = request.user.address
        form = CheckoutForm(initial=initial)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def payment(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.payment_status == Order.PAYMENT_PAID:
        return redirect('orders:order_detail', pk=order.pk)

    client_secret = request.session.get(f'order_{order.id}_client_secret')
    if not client_secret:
        # На случай, если сессия истекла — просто спросим Stripe заново
        intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent_id)
        client_secret = intent.client_secret

    return render(request, 'orders/payment.html', {
        'order': order,
        'client_secret': client_secret,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    })


@login_required
@require_POST
def payment_success(request, pk):
    """
    Вызывается JS-кодом после того, как Stripe сообщил об успешной оплате
    на фронтенде. Мы не доверяем этому и сами перепроверяем статус
    PaymentIntent через Stripe API — только тогда помечаем заказ оплаченным.
    """
    order = get_object_or_404(Order, pk=pk, user=request.user)
    intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent_id)

    if intent.status == 'succeeded':
        order.payment_status = Order.PAYMENT_PAID
        order.status = Order.STATUS_CONFIRMED
        order.save(update_fields=['payment_status', 'status'])

        Cart(request).clear()

        messages.success(request, f'Order #{order.pk} paid successfully!')
        return JsonResponse({'ok': True, 'redirect_url': f'/orders/{order.pk}/'})

    return JsonResponse({'ok': False, 'error': 'Payment not completed'}, status=400)


@csrf_exempt
def stripe_webhook(request):
    """
    Необязательный, но рекомендуемый эндпоинт. Stripe сам стучится сюда
    и сообщает о статусе платежей — это надёжнее, чем ждать JS-запрос
    выше, потому что сработает даже если пользователь закрыл вкладку
    сразу после оплаты.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        order_id = intent['metadata'].get('order_id')
        if order_id:
            Order.objects.filter(pk=order_id).update(
                payment_status=Order.PAYMENT_PAID,
                status=Order.STATUS_CONFIRMED,
            )

    return HttpResponse(status=200)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if not request.user.is_shop_admin() and order.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('catalog:index')
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


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