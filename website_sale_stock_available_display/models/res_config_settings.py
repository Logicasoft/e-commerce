# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    inventory_availability = fields.Selection(selection_add=[
        ('always_no_lock',
         'Show inventory on website, allow sales if not enough stock and add a message if stock below threshold'),
    ])
