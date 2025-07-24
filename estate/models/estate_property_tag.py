from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _order = "name"
    _sql_constraints = [
        (
            'unique_property_tag_name', 'UNIQUE(name)', 
            'The tag name must be unique.'
        )
    ]

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color Index')
