from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    """username = models.CharField(max_length=50, unique = True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)"""
    dob = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
    

class InterviewResponse(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio/')
    transcript = models.CharField(blank = True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

