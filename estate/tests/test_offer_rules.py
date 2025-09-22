from odoo.tests import tagged
from odoo.exceptions import UserError
from .common import EstateTestCommon


@tagged('post_install', '-at_install')
class TestEstateOfferRules(EstateTestCommon):
    def test_cannot_offer_on_sold_property(self):
        self.property.state = 'sold'
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create({
                'price': 1000000,
                'partner_id': self.partner.id,
                'property_id': self.property.id,
            })
