# Generated by Django 4.1.4 on 2022-12-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asset', '0003_trade_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]