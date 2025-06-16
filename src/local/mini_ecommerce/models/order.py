import random
import string

from odoo import api, fields, models
from odoo.exceptions import UserError


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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name"):
                vals["name"] = self._generate_order_number()
        records = super().create(vals_list)
        return records

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

    # Statusni yangilovchi action methodlar
    def action_confirm(self):
        """Buyurtmani tasdiqlash"""
        for record in self:
            if record.state != "draft":
                raise UserError(
                    "Faqat qoralama holatidagi buyurtmalarni tasdiqlash mumkin!"
                )
            if not record.order_line_ids:
                raise UserError(
                    "Buyurtma qatorlarisiz buyurtmani tasdiqlash mumkin emas!"
                )
            record.state = "confirmed"

    def action_deliver(self):
        """Buyurtmani yetkazilgan deb belgilash"""
        for record in self:
            if record.state != "confirmed":
                raise UserError(
                    "Faqat tasdiqlangan buyurtmalarni yetkazilgan deb belgilash mumkin!"
                )
            record.state = "delivered"

    def action_cancel(self):
        """Buyurtmani bekor qilish"""
        for record in self:
            if record.state == "delivered":
                raise UserError("Yetkazilgan buyurtmani bekor qilish mumkin emas!")
            record.state = "cancelled"

    def action_reset_to_draft(self):
        """Buyurtmani qoralamaga qaytarish"""
        for record in self:
            if record.state == "delivered":
                raise UserError(
                    "Yetkazilgan buyurtmani qoralamaga qaytarish mumkin emas!"
                )
            record.state = "draft"
