import graphene

from ...vendor import models
from .types import Vendor


def resolve_vendors(info, created, status, query, sort_by=None):
    return models.Vendor.objects.all()


def resolve_vendor(info, vendor_id):
    return graphene.Node.get_node_from_global_id(info, vendor_id, Vendor)
