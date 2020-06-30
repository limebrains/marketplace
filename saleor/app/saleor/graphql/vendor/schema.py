import graphene
from .types import Vendor
from .resolvers import resolve_vendor, resolve_vendors


class VendorQueries(graphene.ObjectType):

    vendor = graphene.Field(
        Vendor,
        description="Look up an order by ID.",
        id=graphene.Argument(graphene.ID, description="ID of an order.", required=True),
    )
    vendors = graphene.List(
        of_type=Vendor,
        description="List of orders.",
    )

    def resolve_vendor(self, info, **data):
        return resolve_vendor(info, data.get("id"))

    def resolve_vendors(
        self, info, created=None, status=None, query=None, sort_by=None, **_kwargs
    ):
        return resolve_vendors(info, created, status, query, sort_by)
