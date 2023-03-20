# Generated by Django 4.1.7 on 2023-03-19 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Asset', '0014_produce_delete_market'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
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
                ('image_url', models.CharField(blank=True, max_length=300, null=True)),
                ('type', models.CharField(default='trade', max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('actual_return', models.FloatField(default=0.0)),
                ('check_id', models.CharField(blank=True, max_length=500, null=True)),
                ('paylink', models.CharField(blank=True, max_length=500, null=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProduceInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('produce', models.CharField(max_length=200)),
                ('price', models.FloatField()),
                ('units', models.PositiveIntegerField()),
                ('base_cost', models.FloatField()),
                ('total_cost', models.FloatField()),
                ('image_url', models.CharField(blank=True, max_length=300, null=True)),
                ('payment', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('check_id', models.CharField(blank=True, max_length=500, null=True)),
                ('paylink', models.CharField(blank=True, max_length=500, null=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
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
                ('image_url', models.CharField(blank=True, max_length=300, null=True)),
                ('type', models.CharField(default='farm', max_length=50)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Completed', 'Completed')], default='Pending', max_length=50)),
                ('actual_return', models.FloatField(default=0.0)),
                ('check_id', models.CharField(blank=True, max_length=500, null=True)),
                ('paylink', models.CharField(blank=True, max_length=500, null=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('partner', models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='Asset.partner')),
            ],
        ),
    ]
