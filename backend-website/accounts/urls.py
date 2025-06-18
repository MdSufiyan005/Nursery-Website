from django.urls import path, include
from .views import (
    home, display, SpecificPlant, checkout, cart_view,
    add_to_cart, remove_from_cart, update_cart_quantity,
    order_payment, callback, shipping_details,profile
)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', home, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('display/', display, name='display'),
    path('display/<int:plant_id>/', SpecificPlant, name='SpecificPlant'),
    path('display/<int:plant_id>/checkout/', checkout, name='checkout'),
    path('cart/', cart_view, name='cart_view'),
    path('add-to-cart/<int:plant_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:plant_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-quantity/<int:plant_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('shipping/', shipping_details, name='shipping_details'),
    path('payment/', order_payment, name='order_payment'),
    path('order/callback/', callback, name='payment_callback'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
