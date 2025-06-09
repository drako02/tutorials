from odoo import models, fields


class User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        string="",
        domain=[("state", "in", ["new", "offer_accepted"])],
    )
