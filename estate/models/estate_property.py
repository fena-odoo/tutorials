from odoo import api, models, fields
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)  # reserved: controls visibility
    state = fields.Selection(              # reserved: controls lifecycle stages
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False
    )
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: date.today() + timedelta(days=90),
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type"
    )
    
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        index=True,
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )
# Compute the total area
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area"
    )
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = (property.living_area or 0) + (property.garden_area or 0)
            
# Compute the best offer price
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices) if prices else 0.0

