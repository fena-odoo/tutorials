from odoo import api, fields, models


class SaleBranch(models.Model):
    _name = 'sale.branch'
    _description = 'Sales Branch'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    sequence_id = fields.Many2one(
        'ir.sequence',
        string='Sequence',
        readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            sequence = self.env['ir.sequence'].create({
                'name': f"{vals.get('name')} Sequence",
                'prefix': f"{vals.get('code', '').upper()}-",
                'padding': 4,
                'code': f"sale.branch.{vals.get('code', '').lower()}",
            })
            vals['sequence_id'] = sequence.id
        return super().create(vals_list)

