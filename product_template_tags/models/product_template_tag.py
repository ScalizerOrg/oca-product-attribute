# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplateTag(models.Model):
    _name = "product.template.tag"
    _description = "Product Tag"
    _order = "sequence, name"
    _parent_store = True

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    color = fields.Integer(string="Color Index")
    product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        string="Products",
        relation="product_template_product_tag_rel",
        column1="tag_id",
        column2="product_tmpl_id",
    )
    products_count = fields.Integer(
        string="# of Products", compute="_compute_products_count"
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    parent_id = fields.Many2one("product.template.tag", index=True, ondelete="cascade")
    child_ids = fields.One2many("product.template.tag", "parent_id")
    parent_path = fields.Char(index=True)
    # [MIG v19]: Odoo 19 warns when a compute walks a parent chain unless the
    # target field is declared recursive=True. Redeclare display_name (which
    # would otherwise be the implicit base field) with the recursive flag so
    # _compute_display_name below can safely traverse parent_id.
    display_name = fields.Char(
        compute="_compute_display_name",
        recursive=True,
        store=False,
    )

    _name_uniq = models.Constraint(
        "unique(name, company_id)",
        "Tag name must be unique inside a company",
    )

    @api.depends("product_tmpl_ids")
    def _compute_products_count(self):
        tag_id_product_count = {}
        if self.ids:
            self.env.cr.execute(
                """SELECT tag_id, COUNT(*)
                FROM product_template_product_tag_rel
                WHERE tag_id IN %s
                GROUP BY tag_id""",
                (tuple(self.ids),),
            )
            tag_id_product_count = dict(self.env.cr.fetchall())
        for rec in self:
            rec.products_count = tag_id_product_count.get(rec.id, 0)

    @api.depends("name", "parent_id.display_name")
    def _compute_display_name(self):
        # [MIG v19]: name_get() was removed in Odoo 17. Build the hierarchical
        # "Parent / Child" label via a depends-tracked compute on display_name.
        for tag in self:
            names = []
            current = tag
            while current:
                names.append(current.name or "")
                current = current.parent_id
            tag.display_name = " / ".join(reversed(names))

    @api.model
    def _name_search(self, name, domain=None, operator="ilike", limit=None, order=None):
        # [MIG v19]: _name_search signature changed in Odoo 17/18 (args -> domain,
        # name_get_uid dropped, order added). Keep the original behavior of
        # matching only the last segment of a "A / B / C" user input.
        if name:
            leaf = name.split(" / ")[-1]
            domain = [("name", operator, leaf)] + list(domain or [])
        return super()._name_search(
            name, domain=domain, operator=operator, limit=limit, order=order
        )

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        # [MIG v19]: _check_recursion() was renamed _has_cycle() in Odoo 17
        # (and its meaning inverted — it now returns True when a cycle is
        # detected, instead of False).
        if self._has_cycle("parent_id"):
            raise ValidationError(_("Tags can't be recursive."))
