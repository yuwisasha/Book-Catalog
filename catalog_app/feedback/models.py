from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    email = models.EmailField(blank=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=False)
    phone = PhoneNumberField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
