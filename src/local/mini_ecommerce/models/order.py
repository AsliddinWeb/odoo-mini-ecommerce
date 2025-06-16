import random
import string

from odoo import api, fields, models


class Order(models.Model):
    _name = "mini.order"
    _description = "Order"

    name = fields.Char("Buyurtma nomeri", readonly=True, copy=False)
    customer_id = fields.Many2one("mini.customer", string="Mijoz", required=True)
    total_amount = fields.Float(
        "Umumiy summa", compute="_compute_total_amount", store=True
    )
    date_order = fields.Datetime("Buyurtma sanasi", default=fields.Datetime.now)
    state = fields.Selection(
        [
            ("draft", "Qoralama"),
            ("confirmed", "Tasdiqlangan"),
            ("delivered", "Yetkazilgan"),
            ("cancelled", "Bekor qilingan"),
        ],
        default="draft",
        string="Holati",
    )

    order_line_ids = fields.One2many(
        "mini.order.line", "order_id", string="Buyurtma qatorlari"
    )

    @api.model
    def create(self, vals):
        if not vals.get("name"):
            vals["name"] = self._generate_order_number()
        return super().create(vals)

    def _generate_order_number(self):
        """Buyurtma raqamini generatsiya qilish"""
        while True:
            number = "ORD-" + "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
            if not self.search([("name", "=", number)]):
                return number

    @api.depends("order_line_ids.subtotal")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.order_line_ids)
