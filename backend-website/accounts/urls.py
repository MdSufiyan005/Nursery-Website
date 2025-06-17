from django.urls import path,include
from .views import home,display,SpecificPlant
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',home, name='home'),
    path('display/', display, name='display'),
    path('display/<int:plant_id>/', SpecificPlant, name='SpecificPlant'),
    path('ajax/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
