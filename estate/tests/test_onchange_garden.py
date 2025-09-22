from odoo.tests import tagged, Form
from .common import EstateTestCommon


@tagged('post_install', '-at_install')
class TestGardenOnchange(EstateTestCommon):
    def test_garden_off_resets_fields(self):
        # Create the property using the Form API
        with Form(self.env['estate.property']) as prop_form:
            prop_form.name = "Garden Test"
            prop_form.expected_price = 100000
            prop_form.garden = True
            prop_form.garden_area = 10
            prop_form.garden_orientation = 'north'

        # Save the form to get the actual record
        prop = prop_form.save()

        # Assert initial values
        self.assertEqual(prop.garden_area, 10, "Garden area should be set to 10")
        self.assertEqual(prop.garden_orientation, 'north', "Garden orientation should be set to 'north'")

        # Toggle garden to False and trigger onchange
        prop.garden = False
        prop._onchange_garden()

        # Check that related fields are reset
        self.assertRecordValues(prop, [{
            'garden_area': 0,
            'garden_orientation': False,
        }])
