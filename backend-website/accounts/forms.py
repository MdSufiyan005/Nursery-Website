from django import forms
from data.models import Order
from django.core.validators import RegexValidator

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