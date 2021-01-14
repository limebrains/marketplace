# Generated by Django 3.0.4 on 2021-01-14 13:03

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    def migrate_data_forward(apps, schema_editor):
        Vendor = apps.get_model("vendor", "Vendor")
        for instance in Vendor.objects.all():
            instance.save()  # Will trigger slug update

    def migrate_data_backward(apps, schema_editor):
        pass

    dependencies = [
        ('vendor', '0002_auto_20200629_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from='name',
                                                            unique=True),
        ),
        migrations.RunPython(
            migrate_data_forward,
            migrate_data_backward,
        ),

    ]
