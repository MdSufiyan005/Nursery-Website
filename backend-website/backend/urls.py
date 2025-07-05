from django.contrib import admin
from django.urls import path,include
from accounts.views import profile

urlpatterns = [
    path('secure-access/admin/', admin.site.urls), 
    path('',include('accounts.urls')),  
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('accounts/profile/',profile, name='profile'),
]