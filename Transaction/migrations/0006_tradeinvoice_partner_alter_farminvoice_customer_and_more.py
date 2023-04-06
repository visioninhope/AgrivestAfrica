# Generated by Django 4.1.7 on 2023-04-04 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Asset', '0017_trade_payback_date'),
        ('Transaction', '0005_alter_farminvoice_harvest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeinvoice',
            name='partner',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='Asset.partner'),
        ),
        migrations.AlterField(
            model_name='farminvoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='farminvoice',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Asset.farm'),
        ),
        migrations.AlterField(
            model_name='produceinvoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='produceinvoice',
            name='produce',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Asset.produce'),
        ),
        migrations.AlterField(
            model_name='tradeinvoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tradeinvoice',
            name='trade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Asset.trade'),
        ),
    ]