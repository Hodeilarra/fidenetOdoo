# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sh_disable_follower_confirm_sale = fields.Boolean(
        string='Disable to add followers by Confirm Quotation'
    )

    sh_disable_sale_follower_email = fields.Boolean(
        string='Disable to add Followers by Send by Email'
    )

    sh_disable_follower_salesperson = fields.Boolean(
        string='Disable to add Salesperson as followers',
    )


class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_disable_follower_confirm_sale = fields.Boolean(
        string='Disable to add followers by Confirm Quotation',
        related='company_id.sh_disable_follower_confirm_sale',
        readonly=False
    )

    sh_disable_sale_follower_email = fields.Boolean(
        string='Disable to add Followers by Send by Email',
        related='company_id.sh_disable_sale_follower_email',
        readonly=False
    )

    sh_disable_follower_salesperson = fields.Boolean(
        string='Disable to add Salesperson as followers',
        related='company_id.sh_disable_follower_salesperson',
        readonly=False
    )
