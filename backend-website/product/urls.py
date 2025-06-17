from django.urls import path
from . import views

urlpatterns = [
    path('shop/',views.shop_page,name='shop_page'),
    path('contact/',views.contact_page,name='contact_page'),
]
