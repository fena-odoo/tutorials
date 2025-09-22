# estate/tests/test_property_selling.py
from odoo.tests import tagged
from odoo.exceptions import UserError
from .common import EstateTestCommon


@tagged('post_install', '-at_install')
class TestEstatePropertySelling(EstateTestCommon):
    def test_cannot_sell_without_accepted_offer(self):
        with self.assertRaises(UserError):
            self.property.action_mark_sold()

    def test_can_sell_with_accepted_offer(self):
        offer = self.env['estate.property.offer'].create({
            'price': 600000,
            'partner_id': self.partner.id,
            'property_id': self.property.id,
        })
        offer.action_accept_offer()
        self.property.action_mark_sold()
        self.assertEqual(self.property.state, 'sold')
