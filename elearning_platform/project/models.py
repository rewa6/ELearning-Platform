from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('end_user', 'End User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    subscription_active = models.BooleanField(default=False)
    total_end_users = models.PositiveIntegerField(default=0)

class EndUserAccount(models.Model):
    parent_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='end_users')
    login_id = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    login_timestamp = models.DateTimeField(null=True, blank=True)
    expiration_timestamp = models.DateTimeField(null=True, blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    device_fingerprint = models.CharField(max_length=255, null=True, blank=True)

class ElearningModule(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    zip_file = models.FileField(upload_to='modules/')
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
