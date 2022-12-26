# Generated by Django 4.1.4 on 2022-12-19 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('units', models.PositiveIntegerField()),
                ('profit_range_min', models.FloatField()),
                ('profit_range_max', models.FloatField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('base_cost', models.FloatField()),
                ('service_charge', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('actual_return', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TradeInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_name', models.CharField(max_length=100)),
                ('trade', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('units', models.PositiveIntegerField()),
                ('profit_range_min', models.FloatField()),
                ('profit_range_max', models.FloatField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('base_cost', models.FloatField()),
                ('service_charge', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('pros_min', models.FloatField()),
                ('pros_max', models.FloatField()),
                ('totalreturn_min', models.FloatField()),
                ('totalreturn_max', models.FloatField()),
                ('extra_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('actual_return', models.FloatField(default=0.0)),
                ('payment', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('units', models.PositiveIntegerField()),
                ('profit_range_min', models.FloatField()),
                ('profit_range_max', models.FloatField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('base_cost', models.FloatField()),
                ('service_charge', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('actual_return', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm_name', models.CharField(max_length=100)),
                ('farm', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('units', models.PositiveIntegerField()),
                ('profit_range_min', models.FloatField()),
                ('profit_range_max', models.FloatField()),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('end_date', models.DateField(default=django.utils.timezone.now)),
                ('base_cost', models.FloatField()),
                ('service_charge', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('pros_min', models.FloatField()),
                ('pros_max', models.FloatField()),
                ('totalreturn_min', models.FloatField()),
                ('totalreturn_max', models.FloatField()),
                ('extra_notes', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('actual_return', models.FloatField(default=0.0)),
                ('payment', models.CharField(max_length=100)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]