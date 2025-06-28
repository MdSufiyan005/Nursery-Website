from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from unfold.admin import ModelAdmin
from django.utils import timezone
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus
from django.conf import settings


plant_choices = [
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
    ('Succulent', 'Succulent'),
    ('Cactus', 'Cactus'),
    ('Herb', 'Herb'),
    ('Flowering', 'Flowering'),
    ('Foliage', 'Foliage'),
    ('Tree', 'Tree'),
    ('Shrub', 'Shrub'),
    ('Vine', 'Vine')
]
class Plant(models.Model):
    name = models.CharField(max_length=100)
    Desciption = models.TextField()
    image = models.ImageField(upload_to='plants/', null=True, blank=True)
    Quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    custom_time = models.DateTimeField(default=timezone.now)
    Category = models.CharField(choices=plant_choices)

    def __str__(self):
        return self.name
    
class User_details(AbstractBaseUser):
    user_name = models.CharField(max_length=100, unique=True)
    Phone_number = models.IntegerField()
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.user_name
    


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    plant = models.ForeignKey('Plant', on_delete=models.SET_NULL, null=True)
    plant_name = models.CharField(max_length=254)  # Store name in case plant is deleted
    quantity = models.PositiveIntegerField()
    price = models.FloatField()  # Price at time of purchase

    def __str__(self):
        return f"{self.plant_name} x {self.quantity}"

    def get_total_amount(self):
        return self.quantity * self.price

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=254)
    email = models.EmailField(null=True,blank= True)  # This field was missing
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    amount = models.FloatField()
    status = models.CharField(
        max_length=254, 
        default=PaymentStatus.PENDING,
        choices=[(status, status) for status in [PaymentStatus.PENDING, PaymentStatus.SUCCESS, PaymentStatus.FAILURE]]
    )
    provider_order_id = models.CharField(max_length=40, unique=True)
    payment_id = models.CharField(max_length=36, null=True, blank=True)
    signature_id = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - ₹{self.amount} - {self.status}"

    def update_inventory(self):
        if self.status == PaymentStatus.SUCCESS:
            for item in self.items.all():
                if item.plant:
                    item.plant.Quantity -= item.quantity
                    item.plant.save()

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_amount(self):
        return sum(item.get_total_amount() for item in self.items.all())


class ContactMessage(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)  # Admin reply

    def __str__(self):
        return f"{self.fullname or 'No Name'} - {self.email or 'No Email'}"

class UserShippingDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
    def __str__(self):
        return f"Shipping details for {self.user.username}"