from odoo import api, fields, models


class OrderLine(models.Model):
    _name = "mini.order.line"
    _description = "Order Line"

    order_id = fields.Many2one(
        "mini.order", string="Buyurtma", required=True, ondelete="cascade"
    )
    product_id = fields.Many2one("mini.product", string="Mahsulot", required=True)
    quantity = fields.Float("Miqdori", default=1, required=True)
    price_unit = fields.Float("Birlik narxi", related="product_id.price", store=True)
    subtotal = fields.Float("Oraliq summa", compute="_compute_subtotal", store=True)

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.price
