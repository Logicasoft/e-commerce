# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 LogicaSoft SPRL (<http://www.logicasoft.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_product_product_free_qty(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id('stock.stock_replenishment_product_product_action')
        return action

    @api.onchange('available_threshold')
    def onchange_available_threshold(self):
        if self.available_threshold <= 0:
            self.available_threshold = 1