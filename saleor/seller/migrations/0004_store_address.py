# Generated by Django 2.1.7 on 2019-09-14 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_store_place_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
