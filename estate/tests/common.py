from odoo.tests.common import TransactionCase


class EstateTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Buyer'})
        cls.property = cls.env['estate.property'].create({
            'name': 'Villa Merah',
            'expected_price': 500000,
            'garden': True,
            'living_area': 120,
        })
