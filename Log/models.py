from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
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
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    other_name = models.CharField(max_length=200)
    gender =(
        ('male','male'),
        ('female','female')
    )
    gender = models.CharField(max_length=50, choices=gender)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    email = models.EmailField()
    contact = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    cor = models.CharField(max_length=300)
    profession = models.CharField(max_length=200)
    relationship = (
        ('single','single'),
        ('married', 'married')
    )
    relationship = models.CharField(max_length=50, choices=relationship)
    id_card = (
        ('Passport','Passport'),
        ('National ID','National ID'),
        ('Driver"s  License', 'Driver"s  License')
    )
    id_card = models.CharField(max_length=100, choices=id_card)
    id_number = models.CharField(max_length=200)
    referral_code = models.CharField(max_length=300, blank=True, null=True)
    next_of_kin = models.CharField(max_length=300)
    nok_relation = models.CharField(max_length=300)
    nok_contact = models.CharField(max_length=200)
    id_pic_front = models.ImageField(default='default.jpg', upload_to='profile_pics')
    id_pic_back = models.ImageField(default='default.jpg', upload_to='profile_pics')
    last_updated = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.user}'s profile" 