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

class File(models.Model):
    # id of the file itself
    id = models.BigAutoField(primary_key=True, auto_created=True)
    # the display name of the file
    name = models.CharField(max_length=255)
    # the owner of the file
    userid = models.CharField(max_length=255)
    # the cover imageid that links to the base64 image
    imageid = models.CharField(max_length=255)

    # the fileid that links to the base64 file
    fileid = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Filebase(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    base64 = models.TextField()

    def __str__(self):
        return self.id

class Imagebase(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    base64 = models.TextField()

    def __str__(self):
        return self.id