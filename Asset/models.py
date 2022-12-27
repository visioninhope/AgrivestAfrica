from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from Log.models import User
from phonenumber_field.modelfields import PhoneNumberField

class Trade(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField(default=1)
    service_charge = models.FloatField()
    image = models.ImageField(default='default.jpg', upload_to='trade_pics')
    description = models.TextField(max_length=800)
    ros_min = models.FloatField()
    ros_max = models.FloatField()
    STATUS = (
        ("Available", "Available"),
        ("Unavailable", "Unavailable"),
    )
    status = models.CharField(max_length=40, choices=STATUS, default='Available')
    Farm = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    slug = models.SlugField(max_length=300,blank=True, null=True)
    payback_date = models.DateField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.name)
        if self.payback_date is None:
            self.payback_date = self.end_date + timedelta(days=14)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    contact = PhoneNumberField()
    location = models.CharField(max_length=300)
    date_joined = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300,blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Farm(models.Model):
    name = models.CharField(max_length=300)
    crop = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', upload_to='farmCrop_pics')
    price = models.FloatField()
    service_charge = models.FloatField()
    ros_min = models.FloatField()
    ros_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=800)
    location = models.CharField(max_length=200)
    partners = models.ManyToManyField(Partner)
    STATUS = (
        ("Available", "Available"),
        ("Unavailable", "Unavailable")
    )
    units_total = models.PositiveIntegerField()
    units_left = models.PositiveIntegerField()
    status = models.CharField(max_length=40, choices=STATUS, default="Available")
    slug = models.SlugField(max_length=300,blank=True, null=True)
    payback_date = models.DateField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        if self.payback_date is None:
            self.payback_date = self.end_date + timedelta(days=14)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=300)
    price = models.FloatField(default=1)
    image = models.ImageField(default='default.jpg', upload_to='market_pics')
    description = models.TextField(max_length=800)
    STATUS = (
        ("Available", "Available"),
        ("Unavailable", "Unavailable"),
    )
    status = models.CharField(max_length=40, choices=STATUS, default='Available')
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=300,blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

