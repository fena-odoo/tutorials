from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = "price desc"

    price = fields.Float()
    
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price >= 0)', 'Offer price must be strictly positive.')
    ]
    
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
        store=True,
        readonly=True
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
    related="property_id.property_type_id",
    store=True,
    readonly=True
)
    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() or fields.Date.today()
            offer.validity = (offer.date_deadline - create_date).days
            
    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")

            # Refuse all other offers first
            other_offers = self.search([
                ('property_id', '=', offer.property_id.id),
                ('id', '!=', offer.id)
            ])
            other_offers.write({'status': 'refused'})

            # Accept this offer
            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True
    
    # Create method to ensure no offers lower than existing ones
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price')

            if not property_id:
                raise UserError("Missing property on the offer.")

            existing_offer = self.env['estate.property.offer'].search([
                ('property_id', '=', property_id),
                ('price', '>=', offer_price)
            ], limit=1)

            if existing_offer:
                raise UserError("You cannot create an offer lower than an existing offer.")

        # Actually create the offers
        offers = super().create(vals_list)

        # ✅ Force recompute of the stored related field so offer_count works
        offers._recompute_field('property_type_id')

        # ✅ Set property state to 'offer_received'
        for offer in offers:
            offer.property_id.state = 'offer_received'

        return offers

