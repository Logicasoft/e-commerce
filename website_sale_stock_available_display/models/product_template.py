# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_availability = fields.Selection(selection_add=[
        ('always_no_lock',
         'Show inventory on website, allow sales if not enough stock and add a message if stock below threshold'),
    ])


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _compute_available_quantities_dict(self):
        res, stock_dict = \
            super(ProductProduct, self)._compute_available_quantities_dict()
        for product in self:
            res[product.id]['immediately_usable_qty'] -= \
                stock_dict[product.id]['incoming_qty']
        return res, stock_dict

    @api.depends('virtual_available', 'incoming_qty')
    def _compute_available_quantities(self):
        return super(ProductProduct, self)._compute_available_quantities()
