from Log.models import User
from django.db import models
from django.utils import timezone


class TradeInvoice(models.Model):
    trade_name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.trade_name


class TradeLog(models.Model):
    trade_name = models.CharField(max_length=100)
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
        return self.trade_name


class FarmInvoice(models.Model):
    farm_name = models.CharField(max_length=100)
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

    def __str__(self):
        return self.farm_name


class FarmLog(models.Model):
    farm_name = models.CharField(max_length=100)
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
        return self.farm_name
