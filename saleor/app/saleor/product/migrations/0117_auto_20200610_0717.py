# Generated by Django 3.0.4 on 2020-06-10 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
        ('product', '0116_productvariantvendorlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='vendors',
            field=models.ManyToManyField(blank=True, related_name='products', through='product.ProductVariantVendorListing', to='vendor.Vendor'),
        ),
        migrations.AddField(
            model_name='productvariantvendorlisting',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='listing', to='vendor.Vendor'),
        ),
    ]