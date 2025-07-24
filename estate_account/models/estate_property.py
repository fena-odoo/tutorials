from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_mark_sold(self):
        _logger.info(">>> action_mark_sold override triggered")

        res = super(EstateProperty, self).action_mark_sold()
        _logger.info(">>> Called super(). Now creating invoice(s)")

        for property in self:
            _logger.info(f">>> Processing property: {property.name} (ID: {property.id})")

            if not property.buyer_id:
                _logger.warning(f">>> No buyer_id found for property: {property.name}")
                continue
            else:
                _logger.info(f">>> Buyer ID: {property.buyer_id.id} - {property.buyer_id.name}")

            # Search for a sales journal
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                _logger.warning(">>> No sales journal found. Cannot create invoice.")
                continue
            else:
                _logger.info(f">>> Using journal: {journal.name} (ID: {journal.id})")

            invoice_vals = {
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',  # This is for customer invoices
                'journal_id': journal.id,
            }

            try:
                invoice = self.env['account.move'].sudo().create(invoice_vals)
                _logger.info(f">>> Invoice created: {invoice.name or invoice.id} for property {property.name}")
            except Exception as e:
                _logger.error(f"!!! Failed to create invoice for {property.name}: {str(e)}")

        _logger.info(">>> Finished invoice creation loop")
        return res
