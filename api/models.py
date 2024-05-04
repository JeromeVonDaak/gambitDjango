from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# Create your models here.

# User Model to Login and auth
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
