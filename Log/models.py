from django.db import models
from django.contrib.auth.models import AbstractUser
#from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    is_sponsor = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    is_offtaker = models.BooleanField(default=False)
    email = models.EmailField()

class Sponsor(models.Model):    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username

class Offtaker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return self.user.username