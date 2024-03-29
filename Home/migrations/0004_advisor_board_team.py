# Generated by Django 4.1.7 on 2023-10-08 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('position', models.CharField(max_length=300)),
                ('bio', models.TextField(max_length=3000)),
                ('image', models.ImageField(default='image.jpg', upload_to='team_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('position', models.CharField(max_length=300)),
                ('bio', models.TextField(max_length=3000)),
                ('image', models.ImageField(default='image.jpg', upload_to='team_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('position', models.CharField(max_length=300)),
                ('bio', models.TextField(max_length=3000)),
                ('image', models.ImageField(default='image.jpg', upload_to='team_pics')),
            ],
        ),
    ]
