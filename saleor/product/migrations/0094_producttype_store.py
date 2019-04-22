# Generated by Django 2.1.7 on 2019-04-01 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('product', '0093_product_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttype',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_types', to='seller.Store'),
        ),
    ]
