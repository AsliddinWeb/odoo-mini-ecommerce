from odoo import api, fields, models


class Customer(models.Model):
    _name = "mini.customer"
    _description = "Customer"
    _rec_name = "full_name"

    name = fields.Char("Ismi", required=True)
    surname = fields.Char("Familiyasi", required=True)
    phone = fields.Char("Telefon raqami")
    address = fields.Text("Manzili")
    email = fields.Char("Email manzili")
    full_name = fields.Char("To'liq ismi", compute="_compute_full_name", store=True)

    order_ids = fields.One2many("mini.order", "customer_id", string="Buyurtmalar")
    order_count = fields.Integer("Buyurtmalar soni", compute="_compute_order_count")

    @api.depends("name", "surname")
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.name or ''} {record.surname or ''}".strip()

    @api.depends("order_ids")
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)
