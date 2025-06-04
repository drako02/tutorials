from datetime import date, timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_utils


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    def _default_date_availability(self):
        return date.today() + timedelta(days=90)
    
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK (expected_price > 0)",
            "The expected price should be greater than 0",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "The selling price should be postive",
        ),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=_default_date_availability, string="Available from", copy=False
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(
        readonly=True, copy=False, compute="_compute_selling_price", store=True
    )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("west", "West"),
            ("east", "East"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="new",
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Char(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _order="id desc"

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped("price")
            record.best_price = max(prices) if prices else 0.0

    def set_sold(self):
        for record in self:
            previous_state = record.state

            if previous_state == "cancelled":
                raise UserError("Cancelled properties cannot be sold")
            if previous_state == "sold":
                raise UserError("Already sold")
            record.state = "sold"
            return True

    def set_cancelled(self):
        for record in self:
            previous_state = record.state

            if previous_state == "sold":
                raise UserError("Sold properties cannot be cancelled")

            if previous_state == "cancelled":
                raise UserError("Already cancelled")

            record.state = "cancelled"
            return True

    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        for record in self:
            accepted_prices = record.offer_ids.filtered(
                lambda r: r.status == "accepted"
            ).mapped("price")

            if len(accepted_prices) == 0:
                record.selling_price = 0
                continue

            record.selling_price = accepted_prices[0]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            compare_res = float_utils.float_compare(
                record.selling_price,
                record.expected_price * 0.9,
                4,
            )

            print("compare_res", compare_res)

            has_an_accepted_offer = record.offer_ids.filtered(
                lambda a: a.status == "accepted"
            ).mapped("id")
            if not has_an_accepted_offer:
                continue

            if compare_res == 1 or compare_res == 0:
                continue

            raise ValidationError(
                "The selling price cannot be less than  90% of the expected price"
            )