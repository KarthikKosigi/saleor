# Generated by Django 2.1.7 on 2019-06-05 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_user_is_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_site_manager',
            field=models.BooleanField(default=False),
        ),
    ]
