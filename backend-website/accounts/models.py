from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    username = slugify(instance.user.username)
    return f'user_{username}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts_profile')
    image = models.ImageField(upload_to=user_directory_path, default='img/profile-placeholder.png')

    def __str__(self):
        return self.user.username

# Create your models here.
class ProfileDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiledetail', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # restored unique=True
    contact = models.CharField(max_length=10)
    address = models.TextField()
    pincode = models.CharField(max_length=6, default="000000")
    city = models.CharField(max_length=100,blank=True, default="")
    state=models.CharField(max_length=100,blank=True,default="")

    def __str__(self):
        return self.name