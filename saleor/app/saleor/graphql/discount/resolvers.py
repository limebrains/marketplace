import graphene_django_optimizer as gql_optimizer

from ...discount import models
from ..utils import filter_by_query_param, sort_queryset
from .sorters import SaleSortField, VoucherSortField

VOUCHER_SEARCH_FIELDS = ("name", "code")
SALE_SEARCH_FIELDS = ("name", "value", "type")


def resolve_vouchers(info, query, sort_by=None, **_kwargs):
    user = info.context.user
    qs = models.Voucher.objects.all()
    if not user.is_superuser and user.is_authenticated:
        qs = qs.filter(vendor__admin_account=user)
    qs = filter_by_query_param(qs, query, VOUCHER_SEARCH_FIELDS)
    qs = sort_queryset(qs, sort_by, VoucherSortField)
    return gql_optimizer.query(qs, info)


def resolve_sales(info, query, sort_by=None, **_kwargs):
    user = info.context.user
    qs = models.Sale.objects.all()
    if not user.is_superuser and user.is_authenticated:
        qs = qs.filter(vendor__admin_account=user)
    qs = filter_by_query_param(qs, query, SALE_SEARCH_FIELDS)
    qs = sort_queryset(qs, sort_by, SaleSortField)
    return gql_optimizer.query(qs, info)
