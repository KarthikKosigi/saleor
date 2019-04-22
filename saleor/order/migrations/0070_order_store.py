# Generated by Django 2.0.5 on 2019-04-05 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_store_slug'),
        ('order', '0069_auto_20190225_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='seller.Store'),
        ),
    ]
