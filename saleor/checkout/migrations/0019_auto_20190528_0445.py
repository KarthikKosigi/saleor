# Generated by Django 2.1.7 on 2019-05-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0018_cart_shipping_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='shipping_type',
            field=models.CharField(choices=[('delivery', 'Delivery'), ('pickup', 'Pickup')], default='delivery', max_length=32),
        ),
    ]
