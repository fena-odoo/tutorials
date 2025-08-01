from odoo import fields, Command, models
import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = "estate.property"
    
    invoice_id = fields.Many2one('account.move', string="Invoice")

    def action_mark_sold(self):
        _logger.info(">>> action_mark_sold override triggered")
        
        # Explicit check BEFORE any side-effect
        self.check_access('write')
        
        print(" reached ".center(100, '='))  # Debug log
        
        res = super(EstateProperty, self).action_mark_sold()
        _logger.info(">>> Called super(). Now creating invoice(s)")
        
        for property in self:
            property.check_access('write')
            
            _logger.info(
                f">>> Processing property: {property.name} (ID: {property.id})"
            )
            
            if not property.buyer_id:
                _logger.warning(
                    f">>> No buyer_id found for property: {property.name}"
                )
                continue
            else:
                _logger.info(
                    f">>> Buyer ID: {property.buyer_id.id} - "
                    f"{property.buyer_id.name}"
                )

            # Find sales journal
            journal = self.env['account.journal'].search(
                [('type', '=', 'sale')],
                limit=1
            )
            if not journal:
                _logger.warning(
                    ">>> No sales journal found. Cannot create invoice."
                )
                continue
            else:
                _logger.info(
                    f">>> Using journal: {journal.name} (ID: {journal.id})"
                )

            # Compute values
            commission = property.selling_price * 0.06
            admin_fee = 100.00

            # Create the invoice with two lines
            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': f"6% Commission for {property.name}",
                        'quantity': 1,
                        'price_unit': commission,
                    }),
                    Command.create({
                        'name': "Administrative Fee",
                        'quantity': 1,
                        'price_unit': admin_fee,
                    }),
                ],
            }

            try:
                invoice = self.env['account.move'].sudo().create(invoice_vals)
                property.invoice_id = invoice
                _logger.info(
                    f">>> Invoice created: {invoice.name or invoice.id} "
                    f"for property {property.name}"
                )
            except Exception as e:
                _logger.error(
                    f"!!! Failed to create invoice for {property.name}: "
                    f"{str(e)}"
                )

        return res
