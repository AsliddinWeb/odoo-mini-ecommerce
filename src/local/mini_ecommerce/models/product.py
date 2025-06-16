from odoo import fields, models


class Product(models.Model):
    _name = "mini.product"
    _description = "Product"

    name = fields.Char("Nomi", required=True)
    price = fields.Float("Narxi", required=True)
    category_id = fields.Many2one("mini.category", string="Toifasi", required=True)
    image = fields.Binary("Rasmi")

    order_line_ids = fields.One2many(
        "mini.order.line", "product_id", string="Buyurtma qatorlari"
    )
