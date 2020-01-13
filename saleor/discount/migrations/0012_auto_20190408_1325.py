# Generated by Django 2.0.5 on 2019-04-08 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_store_slug'),
        ('discount', '0011_auto_20180803_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='seller.Store'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='seller.Store'),
        ),
    ]