from django.contrib import admin
from django.core.mail import send_mail
from .models import ContactMessage

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

