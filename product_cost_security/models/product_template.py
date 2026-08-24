# Copyright 2018 Sergio Teruel - Tecnativa <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "product.cost.security.mixin"]

    # Inherited fields
    # purchase.group_purchase_user is included here (not just via implied_ids in a
    # downstream module) because core purchase's own view_product_supplier_inherit
    # (which shows seller_ids to purchase.group_purchase_user, whose context reads
    # standard_price) is validated while purchase's own data loads, on a fresh
    # install - strictly before any module that only *depends on* purchase (like a
    # downstream security module) gets to contribute its groups override. Only a
    # module that loads no later than purchase itself - as this one structurally
    # does - can prevent that "Access Rights Inconsistency" warning at its source.
    # A purchase user legitimately needs to see a vendor's default cost (2026-08-24).
    standard_price = fields.Float(
        groups="product_cost_security.group_product_cost,purchase.group_purchase_user"
    )
