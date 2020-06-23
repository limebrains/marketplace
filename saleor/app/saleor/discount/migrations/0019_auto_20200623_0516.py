# Generated by Django 3.0.4 on 2020-06-23 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        ('discount', '0018_auto_20190827_0315'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.Vendor', verbose_name='sales'),
        ),
        migrations.AddField(
            model_name='voucher',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendor.Vendor', verbose_name='vouchers'),
        ),
    ]
