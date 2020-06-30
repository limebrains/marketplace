from django.db import models
from versatileimagefield.fields import VersatileImageField
from ..account.models import User
from ..core.models import (
    ModelWithMetadata,
)


class Vendor(ModelWithMetadata):
    name = models.CharField(max_length=250)
    avatar = VersatileImageField(upload_to="vendor-avatars", blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    admin_account = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )


class VendorLocation(ModelWithMetadata):
    country = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    zip_code = models.CharField(max_length=250)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
