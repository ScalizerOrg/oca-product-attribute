# Copyright 2018 Sergio Teruel - Tecnativa <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "product.cost.security.mixin"]

    # Inherited fields
    # See product_template.py for the full rationale: purchase.group_purchase_user
    # must be included here directly (not only via a downstream implied_ids grant)
    # so that core purchase's own view_product_product_supplier_inherit validates
    # cleanly on a fresh install (2026-08-24).
    standard_price = fields.Float(
        groups="product_cost_security.group_product_cost,purchase.group_purchase_user"
    )
