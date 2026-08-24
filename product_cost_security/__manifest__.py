# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Cost Security",
    "summary": "Product cost security restriction view",
    "version": "19.0.1.0.0",
    "development_status": "Production/Stable",
    "maintainers": ["sergio-teruel", "rafaelbn", "yajo"],
    "category": "Product",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    # purchase (2026-08-24): the field-level groups= override on standard_price
    # references purchase.group_purchase_user by xmlid (see models/product_template.py
    # and models/product_product.py) - without a real dependency edge, this module's
    # own load order relative to purchase is only decided by an alphabetical
    # tie-break, which happened to put it BEFORE purchase, so purchase's own xmlids
    # (e.g. its groups) were not registered yet when this module's code referenced
    # them - breaking both this module's own tests and, on a fresh install, any
    # runtime access check on standard_price performed before purchase loads.
    "depends": ["product", "purchase"],
    "data": ["security/product_cost_security.xml", "views/product_views.xml"],
}
