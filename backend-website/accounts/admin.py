from django.contrib import admin
from .models import ProfileDetail
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username', 'user__email')

admin.site.register(UserProfile, UserProfileAdmin)

@admin.register(ProfileDetail)
class ProfileDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'pincode')
    search_fields = ('name', 'email', 'pincode')