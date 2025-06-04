from odoo import models, fields

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    _sql_constraints = [
        ("check_type_name", "UNIQUE (name)", "This type name has already been used"),
    ]

    name = fields.Char(required=True)
    sequence=fields.Integer("Sequence", default=1, help="Used to order property types")
    property_ids = fields.One2many("estate.property", "property_type_id", string="Property")

    _order="sequence,name"

