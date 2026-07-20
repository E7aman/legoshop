from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('payment/<int:pk>/success/', views.payment_success, name='payment_success'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('history/', views.order_history, name='order_history'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    # Admin
    path('admin/', views.admin_order_list, name='admin_order_list'),
    path('admin/<int:pk>/', views.admin_order_detail, name='admin_order_detail'),
]