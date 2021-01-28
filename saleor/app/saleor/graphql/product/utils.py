from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List

import graphene
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError

from ...product import AttributeInputType
from ...product.error_codes import ProductErrorCode
from ...warehouse.models import Stock

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from ...product.models import Attribute, ProductVariant


def validate_attribute_input_for_product(instance: "Attribute", values: List[str]):
    if not values:
        if not instance.value_required:
            return
        raise ValidationError(
            f"{instance.slug} expects a value but none were given",
            code=ProductErrorCode.REQUIRED.value,
        )

    if instance.input_type != AttributeInputType.MULTISELECT and len(values) != 1:
        raise ValidationError(
            f"A {instance.input_type} attribute must take only one value",
            code=ProductErrorCode.INVALID.value,
        )

    for value in values:
        if not value.strip():
            raise ValidationError(
                "Attribute values cannot be blank", code=ProductErrorCode.REQUIRED.value
            )


def validate_attribute_input_for_variant(instance: "Attribute", values: List[str]):
    if not values:
        raise ValidationError(
            f"{instance.slug} expects a value but none were given",
            code=ProductErrorCode.REQUIRED.value,
        )

    if len(values) != 1:
        raise ValidationError(
            f"A variant attribute cannot take more than one value",
            code=ProductErrorCode.INVALID.value,
        )

    if not values[0].strip():
        raise ValidationError(
            "Attribute values cannot be blank", code=ProductErrorCode.REQUIRED.value
        )


def get_used_attibute_values_for_variant(variant):
    """Create a dict of attributes values for variant.

    Sample result is:
    {
        "attribute_1_global_id": ["ValueAttr1_1"],
        "attribute_2_global_id": ["ValueAttr2_1"]
    }
    """
    attribute_values = defaultdict(list)
    for assigned_variant_attribute in variant.attributes.all():
        attribute = assigned_variant_attribute.attribute
        attribute_id = graphene.Node.to_global_id("Attribute", attribute.id)
        for variant in assigned_variant_attribute.values.all():
            attribute_values[attribute_id].append(variant.slug)
    return attribute_values


def get_used_variants_attribute_values(product, vendor):
    """Create list of attributes values for all existing `ProductVariants` for product.

    Sample result is:
    [
        {
            "attribute_1_global_id": ["ValueAttr1_1"],
            "attribute_2_global_id": ["ValueAttr2_1"]
        },
        ...
        {
            "attribute_1_global_id": ["ValueAttr1_2"],
            "attribute_2_global_id": ["ValueAttr2_2"]
        }
    ]
    """
    variants = (
        product.variants.prefetch_related("attributes__values")
        .prefetch_related("attributes__assignment")
        .filter(vendor__name=vendor)
    )
    used_attribute_values = []
    for variant in variants:
        attribute_values = get_used_attibute_values_for_variant(variant)
        used_attribute_values.append(attribute_values)
    return used_attribute_values


@transaction.atomic
def update_or_create_stocks(
    variant: "ProductVariant", stocks_data: List[Dict[str, str]], warehouses: "QuerySet"
):
    try:
        for stock_data, warehouse in zip(stocks_data, warehouses):
            Stock.objects.update_or_create(
                    defaults=dict(quantity=stock_data["quantity"]),
                    product_variant=variant,
                    warehouse=warehouse,
                )
    except IntegrityError as e:
        print(f"---\nerror in update_or_create_stocks:\n{e}\n---")
        msg = "Stock for one of warehouses already exists for this product variant."
        raise ValidationError(msg)
