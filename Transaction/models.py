from Log.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TradeInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    trade = models.CharField(max_length=200)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    service_charge = models.FloatField()
    total_cost = models.FloatField()
    pros_min = models.FloatField()
    pros_max = models.FloatField()
    totalreturn_min = models.FloatField()
    totalreturn_max = models.FloatField()
    extra_notes = models.CharField(max_length=200, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=50, default='trade')
    ##roll on option
    #when user started trade
        #hide in trade logs interval b/n start and finish//
    
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default='Pending')
    start_time = models.DateTimeField(default=timezone.now)
    actual_return = models.FloatField(default=0.00)
    payment = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class TradeLog(models.Model):
    name = models.CharField(max_length=300)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    service_charge = models.FloatField()
    total_cost = models.FloatField()
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default='Pending')
    start_time = models.DateTimeField(default=timezone.now)
    actual_return = models.FloatField(default=0.00)

    def __str__(self):
        return self.name


class FarmInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    service_charge = models.FloatField()
    total_cost = models.FloatField()
    pros_min = models.FloatField()
    pros_max = models.FloatField()
    totalreturn_min = models.FloatField()
    totalreturn_max = models.FloatField()
    extra_notes = models.CharField(max_length=200, blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=50, default='farm')
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default='Pending')
    start_time = models.DateTimeField(default=timezone.now)
    actual_return = models.FloatField(default=0.00)
    payment = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name


class FarmLog(models.Model):
    name = models.CharField(max_length=300)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    service_charge = models.FloatField()
    total_cost = models.FloatField()
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default='Pending')
    start_time = models.DateTimeField(default=timezone.now)
    actual_return = models.FloatField(default=0.00)

    def __str__(self):
        return self.name



class TradeReceipt(models.Model):
    token = models.UUIDField(max_length=300,default=1,unique=True)
    trade = models.ForeignKey(TradeInvoice,on_delete=models.CASCADE)
    check_id = models.CharField(max_length=500, unique=True)
    paylink = models.CharField(max_length=500)
    status = (
        ('unpaid','unpaid'),
        ('paid','paid')
    )
    status = models.CharField(max_length=50, choices=status, default='unpaid')
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.trade.name
    

class ProduceInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    produce = models.CharField(max_length=200)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    base_cost = models.FloatField()
    total_cost = models.FloatField()
    image_url = models.CharField(max_length=300, blank=True, null=True)
    payment = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class ProduceLog(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    produce = models.CharField(max_length=200)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    base_cost = models.FloatField()
    total_cost = models.FloatField()
    payment = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

