import graphene

from ...vendor import models
from .types import Vendor


def resolve_vendors(info, created, status, query, sort_by=None):
    return models.Vendor.objects.all()


def resolve_vendor(info, vendor_id, vendor_slug=None):
    if vendor_slug:
        try:
            vendor_model = models.Vendor.objects.get(slug=vendor_slug)
        except models.Vendor.DoesNotExist as e:
            print(f"---\nerror in resolve_vendor:\n{e}\n---")
            vendor_model = None
        return vendor_model
    return graphene.Node.get_node_from_global_id(info, vendor_id, Vendor)
