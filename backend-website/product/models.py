from django.db import models

class ContactMessage(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)  # Admin reply

    def __str__(self):
        return f"{self.fullname or 'No Name'} - {self.email or 'No Email'}"
