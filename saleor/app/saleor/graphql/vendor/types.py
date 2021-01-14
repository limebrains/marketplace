import graphene
from graphene import relay

from ...vendor import models
from ..core.types import Image
from ..core.connection import CountableDjangoObjectType


class Vendor(CountableDjangoObjectType):
    name = graphene.String(description="Name of the vendor.")
    slug = graphene.String(description="Name of the vendor without spaces.")
    avatar = graphene.Field(Image, size=graphene.Int(description="Size of the avatar."))
    description = graphene.String(description="Name of the vendor.")
    address = graphene.Field(lambda: VendorLocation, description="Vendor locations.")

    class Meta:
        description = (
            "Vendor allows having multiple sources of same product."
        )
        interfaces = [relay.Node]
        model = models.Vendor
        only_fields = ["name", "address"]

    @staticmethod
    def resolve_name(root: models.Vendor, *_args, **_kwargs):
        return root.name

    @staticmethod
    def resolve_slug(root: models.Vendor, *_args, **_kwargs):
        return root.slug

    @staticmethod
    def resolve_description(root: models.Vendor, *_args, **_kwargs):
        return root.description

    @staticmethod
    def resolve_address(root: models.Vendor, info, **_kwargs):
        return root.address_set.all()

    @staticmethod
    def resolve_avatar(root: models.User, info, size=None, **_kwargs):
        if root.avatar:
            return Image.get_adjusted(
                image=root.avatar,
                alt=None,
                size=size,
                rendition_key_set="vendor_avatars",
                info=info,
            )


class VendorLocation(CountableDjangoObjectType):
    country = graphene.String(description="Country.")
    city = graphene.String(description="City.")
    zip_code = graphene.String(description="Zip code.")
    address1 = graphene.String(description="Address, first line.")
    address2 = graphene.String(description="Address, second line.")
    name = graphene.String(description="Name of the location.")
    description = graphene.String(description="Description of a location.")
    vendor = graphene.Field(lambda: Vendor, description="Owner of the location.", required=False)

    class Meta:
        description = (
            "Address for a vendor."
        )
        only_fields = [
            "country",
            "city",
            "zip_code",
            "address1",
            "address2",
            "name",
            "description",
            "vendor",
        ]
        interfaces = [relay.Node]
        model = models.VendorLocation

    @staticmethod
    def resolve_country(root: models.VendorLocation, _info):
        return root.country

    @staticmethod
    def resolve_city(root: models.VendorLocation, _info):
        return root.city

    @staticmethod
    def resolve_zip_code(root: models.VendorLocation, _info):
        return root.zip_code

    @staticmethod
    def resolve_address1(root: models.VendorLocation, _info):
        return root.address1

    @staticmethod
    def resolve_address2(root: models.VendorLocation, _info):
        return root.address2

    @staticmethod
    def resolve_name(root: models.VendorLocation, _info):
        return root.name

    @staticmethod
    def resolve_description(root: models.VendorLocation, _info):
        return root.description

    @staticmethod
    def resolve_vendor(root: models.VendorLocation, _info):
        return root.vendor if root.vendor else None
