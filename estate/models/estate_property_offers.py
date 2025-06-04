from datetime import date, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError



class PropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    _sql_constraints = [
        ("check_price", "CHECK (price > 0)", "The price should be greater than 0"),
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )

    _order="price desc"

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date
            if create_date:
                record.date_deadline = create_date.date() + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = (
                offer.create_date.date() if offer.create_date else date.today()
            )
        if offer.date_deadline:
            deadline = offer.date_deadline
            if isinstance(deadline, str):
                deadline = fields.Date.from_string(deadline)
            offer.validity = (deadline - create_date).days
        else:
            offer.validity = 0

    def accept_offer(self):
        for record in self:
            accepted_offers = record.property_id.offer_ids.filtered(
                lambda r: r.status == "accepted"
            ).mapped("price")

            if len(accepted_offers) == 1:
                raise UserError("An offer has already been accepted")

            record.status = "accepted"
            return True

    def refuse_offer(self):
        for record in self:
            record.status = "refused"
            return True
    
