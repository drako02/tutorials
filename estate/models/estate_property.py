from datetime import date, timedelta
from odoo import models, fields, api

class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def _default_date_availability(self):
        return date.today() + timedelta(days=90)
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0  


    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=_default_date_availability, string="Available from", copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ( "west", "West"), ("east", "East")])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[("new", "New"), ("offer_received", "Offer Received"), ( "offer_accepted", "Offer Accepted"), ("sold", "Sold"),("cancelled", "cancelled")], required=True, default="new", copy=False)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users",string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Char(compute="_compute_total_area") 
    best_price = fields.Float(compute="_compute_best_price")

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(required=True)

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(required=True)

class PropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"


    price = fields.Float()
    status = fields.Selection(selection=[("accepted", "Accepted"), ("refused", "Refused")],copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")


    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date
            if create_date:
                record.date_deadline = create_date.date() + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else date.today()
        if offer.date_deadline:
            deadline = offer.date_deadline
            if isinstance(deadline, str):
                deadline = fields.Date.from_string(deadline)
            offer.validity = (deadline - create_date).days
        else:
            offer.validity = 0