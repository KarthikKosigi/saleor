# Generated by Django 2.1.7 on 2019-05-22 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_store_slug'),
        ('site', '0020_auto_20190301_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_settings', to='seller.Store'),
        ),
    ]
