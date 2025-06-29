from django import forms
from .models import ContactMessage
# from .models import UserShippingDetails
from django import forms
from data.models import Order
from django.core.validators import RegexValidator
from .models import ProfileDetail

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('fullname', 'email', 'message')


# class ShippingDetailsForm(forms.ModelForm):
#     class Meta:
#         model = UserShippingDetails
#         exclude = ['user']

# from .models import ProfileDetail
# class ProfileDetailForm(forms.ModelForm):
#     class Meta:
#         model = ProfileDetail
#         fields = ('name', 'email', 'contact', 'address')


class ShippingDetailsForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be 10 digits"
    )
    
    phone_number = forms.CharField(validators=[phone_regex])
    pincode = forms.CharField(max_length=6, min_length=6)

    class Meta:
        model = Order
        fields = ['name', 'email', 'phone_number', 'address', 'city', 'state', 'pincode']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['name'].initial = user.get_full_name() or user.username
            self.fields['email'].initial = user.email
            
class ProfileDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['email'].initial = user.email
            if not self.instance.pk:
                self.fields['name'].initial = user.get_full_name() or user.username

    class Meta:
        model = ProfileDetail
        fields = ('name', 'email', 'contact', 'address', 'pincode')