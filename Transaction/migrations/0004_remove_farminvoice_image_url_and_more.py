# Generated by Django 4.1.7 on 2023-04-03 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0003_remove_farminvoice_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farminvoice',
            name='image_url',
        ),
        migrations.RemoveField(
            model_name='tradeinvoice',
            name='image_url',
        ),
    ]
