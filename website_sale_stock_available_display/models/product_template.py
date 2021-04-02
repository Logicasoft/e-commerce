# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection(selection_add=[
        ('always_no_lock',
         'Show inventory on website, allow sales if not enough stock and add a message if stock below threshold'),
    ])

    @api.onchange('available_threshold')
    def onchange_available_threshold(self):
        if self.available_threshold <= 0:
            self.available_threshold = 1

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(
            combination=combination, product_id=product_id, add_qty=add_qty, pricelist=pricelist,
            parent_combination=parent_combination, only_template=only_template)

        if not self.env.context.get('website_sale_stock_get_quantity'):
            return combination_info

        if combination_info['product_id']:
            product = self.env['product.product'].sudo().browse(combination_info['product_id'])
            website = self.env['website'].get_current_website()
            virtual_available = product.with_context(warehouse=website.warehouse_id.id).virtual_available
            free_qty = product.with_context(warehouse=website.warehouse_id.id).free_qty
            combination_info.update({
                'virtual_available': virtual_available,
                'virtual_available_formatted': self.env['ir.qweb.field.float'].value_to_html(virtual_available, {'precision': 0}),
                'free_qty': free_qty,
                'free_qty_formatted': self.env['ir.qweb.field.float'].value_to_html(free_qty, {'precision': 0}),
                'product_type': product.type,
                'inventory_availability': product.inventory_availability,

                'available_threshold': product.available_threshold,
                'custom_message': product.custom_message,
                'product_template': product.product_tmpl_id.id,
                'cart_qty': product.cart_qty,
                'uom_name': product.uom_id.name,
            })
        else:
            product_template = self.sudo()
            combination_info.update({
                'virtual_available': 0,
                'product_type': product_template.type,
                'inventory_availability': product_template.inventory_availability,
                'available_threshold': product_template.available_threshold,
                'custom_message': product_template.custom_message,
                'product_template': product_template.id,
                'cart_qty': 0
            })

        return combination_info
