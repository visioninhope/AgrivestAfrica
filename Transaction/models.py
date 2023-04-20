from Log.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from Asset.models import Partner,Trade,Farm,Produce


class TradeInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    trade = models.ForeignKey(Trade, on_delete=models.PROTECT)
    partner  = models.ForeignKey(Partner, on_delete=models.PROTECT, default=2)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    # service_charge = models.FloatField()
    total_cost = models.FloatField()
    pros_min = models.FloatField()
    pros_max = models.FloatField()
    totalreturn_min = models.FloatField()
    totalreturn_max = models.FloatField()
    extra_notes = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=50, default='trade')
    HarvestType = (
        ('Cash','Cash'),
        ('Roll on trade','Roll on trade'),
        ('Crop', 'Crop')
    )
    harvest_type = models.CharField(max_length=50, choices=HarvestType, default='Cash')
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(max_length=50, choices=CHOICES, default='Pending')
    actual_return = models.FloatField(default=0.00)
    #token = models.UUIDField(max_length=300,default=1)
    check_id = models.CharField(max_length=500, blank=True, null=True)
    paylink = models.CharField(max_length=500, blank=True,null=True)
    start_time = models.DateTimeField(default=timezone.now, blank=True, null=True)

    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

class FarmInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT)
    partner  = models.ForeignKey(Partner, on_delete=models.PROTECT, default=2)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    profit_range_min = models.FloatField()
    profit_range_max = models.FloatField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    base_cost = models.FloatField()
    # service_charge = models.FloatField()
    total_cost = models.FloatField()
    pros_min = models.FloatField()
    pros_max = models.FloatField()
    totalreturn_min = models.FloatField()
    totalreturn_max = models.FloatField()
    extra_notes = models.CharField(max_length=200, blank=True, null=True)
    HarvestType = (
        ('Cash','cash'),
        ('Roll on trade','roll on trade'),
        ('Crop', 'crop')
    )
    harvest_type = models.CharField(max_length=50, choices=HarvestType)
    type = models.CharField(max_length=50, default='farm')
    CHOICES = (
        ("Pending", "Pending"),
        ("Active", "Active"),
        ("Completed", "Completed")
    )
    status = models.CharField(max_length=50, choices=CHOICES, default='Pending')
    actual_return = models.FloatField(default=0.00)
    check_id = models.CharField(max_length=500, blank=True, null=True)
    #token = models.UUIDField(max_length=300,default=1)
    paylink = models.CharField(max_length=500, blank=True,null=True)
    start_time = models.DateTimeField(default=timezone.now, blank=True, null=True)

    slug = models.SlugField(max_length=250, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

    
class ProduceInvoice(models.Model):
    name = models.CharField(max_length=100,unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    # produce = models.CharField(max_length=200)
    produce = models.ForeignKey(Produce, on_delete=models.PROTECT)
    price = models.FloatField()
    units = models.PositiveIntegerField()
    base_cost = models.FloatField()
    total_cost = models.FloatField()
    image_url = models.CharField(max_length=300, blank=True, null=True)
    slug = models.SlugField(max_length=250, blank=True, null=True)
    CHOICES = (
        ("Pending", "Pending"),
        ("Completed", "Completed")
    )
    status = models.CharField(
        max_length=50, choices=CHOICES, default='Pending')
    check_id = models.CharField(max_length=500, blank=True, null=True)
    paylink = models.CharField(max_length=500, blank=True,null=True)
    start_time = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.slug == None:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name

