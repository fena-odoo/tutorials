from odoo import _, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_product_info_pos(self, price, quantity, pos_config_id):
        """
        override the get_product_info_pos method in the product.product include volume and weight.
        """
        product_info = super(ProductProduct, self).get_product_info_pos(price, quantity, pos_config_id)
        
        product_info.update({
            'volume': self.volume or 0.0,
            'weight': self.weight or 0.0,
        })
        
        return product_info

    # def _loader_params_pos_config(self):
    #     res = super()._loader_params_pos_config()
    #     res['fields'].append('congratulatory_text')
    #     return res
