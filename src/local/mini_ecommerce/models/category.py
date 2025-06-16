from odoo import api, fields, models


class Category(models.Model):
    _name = "mini.category"
    _description = "Product Category"

    name = fields.Char("Nomi", required=True)
    description = fields.Text("Tavsifi")

    product_ids = fields.One2many("mini.product", "category_id", string="Mahsulotlar")
    product_count = fields.Integer("Mahsulotlar soni", compute="_compute_product_count")

    @api.depends("product_ids")
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)
