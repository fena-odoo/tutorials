from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"
    _sql_constraints = [
        (
            'check_expected_price_positive',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.'
        ),
        (
            'check_selling_price_positive',
            'CHECK(selling_price >= 0)',
            'The selling price must be positive.'
        )
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
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
    total_area = fields.Integer(
        string="Total Area (sqm)",
        compute="_compute_total_area"
    )
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company
    )
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price"
    )
    user_id = fields.Many2one('res.users', string="Assigned User")
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
        # default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string="Offers"
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default='new',
        required=True,
        copy=False,
        string="Status"
    )
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )

    # Compute the total area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = (
                (property.living_area or 0) + (property.garden_area or 0)
            )

    # Compute the best offer price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            prices = property.offer_ids.mapped('price')
            property.best_price = max(prices) if prices else 0.0

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price_margin(self):
        for record in self:
            if not record.selling_price:
                continue  # Do not validate if no offer is accepted yet
            min_price = record.expected_price * 0.9
            if float_compare(
                record.selling_price, min_price, precision_digits=2
            ) < 0:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of the expected price. "
                    "If you want to set a lower price, please adjust the expected price first."
                )

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

# Deletion constraint to prevent deletion of properties in certain states
    @api.ondelete(at_uninstall=False)
    def _check_deletable_state(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError(
                    "You can only delete properties that are New or Cancelled."
                )

# Action methods for property sold or rejected          
    def action_mark_sold(self):
        for property in self:
            if property.state == 'cancelded':
                raise UserError("Cancelled properties cannot be sold.")
            if not property.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError("You can't sell a property with no accepted offer.")
            property.state = 'sold'
        return True

    def action_cancel_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("Sold properties cannot be cancelled.")
            property.state = 'cancelled'
        return True

