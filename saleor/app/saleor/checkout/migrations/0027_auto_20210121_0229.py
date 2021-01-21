# Generated by Django 3.0.4 on 2021-01-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0026_checkoutline_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkoutline',
            name='vendor',
        ),
        migrations.AddField(
            model_name='checkoutline',
            name='vendor_name',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
