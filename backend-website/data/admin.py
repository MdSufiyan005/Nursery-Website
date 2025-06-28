from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin  # <-- using Unfold's ModelAdmin
from unfold.contrib.import_export.forms import (ExportForm, ImportForm)
from unfold.forms import (AdminPasswordChangeForm, UserChangeForm,
                          UserCreationForm)
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter

from .models import Plant, User_details,Order, OrderItem,ContactMessage,UserShippingDetails

from django.core.mail import send_mail

admin.site.register(UserShippingDetails)

# admin.site.register(Plant)
# admin.site.register(User_details)
# Register your models here.
admin.site.unregister(User) # Unregister the default User model to customize it
# admin.site.register(Order) # Register the Order model
@register(User)
class UserAdmin(BaseUserAdmin,ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Plant)
class PlantAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('name', 'Category', 'price', 'Quantity', 'created_at')
    list_filter = ('Category',)
    search_fields = ('name', 'Category', 'Desciption')
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'Category', 'price', 'Quantity')
        }),
        ('Description & Media', {
            'fields': ('Desciption', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True 
    list_filter = ['Category',
                   ("created_at", RangeDateFilter)]

@admin.register(User_details)
class UserAdmin(ModelAdmin):
    list_display = ('user_name', 'email', 'Phone_number')
    search_fields = ('user_name', 'email')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('plant_name', 'quantity', 'price')
    can_delete = False
    extra = 0

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'name', 'amount', 'status', 'created_at')
    list_filter = ('status', ('created_at', RangeDateFilter))
    search_fields = ('id', 'name', 'provider_order_id', 'payment_id')
    readonly_fields = ('id', 'provider_order_id', 'payment_id', 'signature_id', 'amount')
    inlines = [OrderItemInline]
    
    def has_add_permission(self, request):
        return False  # Orders should only be created through the payment process

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'submitted_at')
    readonly_fields = ('submitted_at',)
    ordering = ('-submitted_at',)
    fields = ('fullname', 'email', 'message', 'response', 'submitted_at')

    def save_model(self, request, obj, form, change):
        if 'response' in form.changed_data and obj.response:
            subject = "Reply from Rudra Flower Nursery 🌸"
            message = f"Dear {obj.fullname},\n\n{obj.response}\n\nRegards,\nRudra Nursery Team"
            from_email = 'your_email@example.com'
            recipient_list = [obj.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                self.message_user(request, f"❌ Error sending email: {e}", level='error')
            else:
                self.message_user(request, f"✅ Email sent to {obj.email}", level='success')

        super().save_model(request, obj, form, change)