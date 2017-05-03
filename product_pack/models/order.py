# -*- coding: utf-8 -*-

from odoo import api, models, fields


class ProductPackSelect(models.TransientModel):
    _name = 'product.pack.select'

    product_id = fields.Many2one('product.product', string='Combo', required=True)

    @api.multi
    def add_pack(self):
        sol_obj = self.env['sale.order.line']
        self.ensure_one()
        order_id = self.env.context.get('active_id')
        for line in self.product_id.pack_line_ids:
            line_order = sol_obj.create(
                self.prepare_sale_order_line_data(order_id, line)
            )
            line_order.name = '[%s] %s' % (self.product_id.name, line_order.name)
        return True

    def prepare_sale_order_line_data(self, order_id, line):
        return {
            'order_id': order_id,
            'product_id': line.product_id.id,
            'product_uom_qty': line.quantity,
            'product_uom': line.product_id.uom_id.id,
            'discount': line.discount
        }
