from odoo import models, fields


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    _sql_constraints = [
        ("check_tag_name", "UNIQUE (name)", "This tag name has already been used"),
    ]

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _order = "name"
