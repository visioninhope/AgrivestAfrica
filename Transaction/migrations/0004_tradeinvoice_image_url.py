# Generated by Django 4.1.7 on 2023-02-24 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transaction', '0003_tradelog_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeinvoice',
            name='image_url',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]