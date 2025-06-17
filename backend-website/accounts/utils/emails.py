from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation(order, user):
    """Send order confirmation email"""
    try:
        context = {
            'order': order,
            'user': user
        }
        
        html_content = render_to_string('emails/order_confirmation.html', context)
        
        email = EmailMessage(
            subject=f'🪴 Order Confirmation #{order.id} - Your Plants are on the Way!',
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False