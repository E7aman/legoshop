from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('legoshop.catalog.urls')),
    path('accounts/', include('legoshop.accounts.urls')),
    path('cart/', include('legoshop.cart.urls')),
    path('orders/', include('legoshop.orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
