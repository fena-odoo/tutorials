from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'  # <-- extension inheritance (modifies res.users in-place)

    property_ids = fields.One2many(
        comodel_name='estate.property',
        inverse_name='salesperson_id',  # <-- Replace this with your actual field
        string='Properties',
        domain=[('state', '=', 'new')]  # Only show properties that are still available
    )
