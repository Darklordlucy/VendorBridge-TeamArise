from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    x_is_vendor = fields.Boolean('Is Vendor', default=False, index=True)
    x_gst_number = fields.Char('GST Number', size=15)
    x_vendor_category = fields.Selection([
        ('it_hardware', 'IT Hardware'),
        ('office_supplies', 'Office Supplies'),
        ('furniture', 'Furniture'),
        ('logistics', 'Logistics'),
        ('stationery', 'Stationery'),
    ], string='Vendor Category', default='office_supplies')
    x_vendor_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
    ], string='Vendor Status', default='active')
    x_rating = fields.Float('Rating', compute='_compute_rating', store=True, digits=(2, 1))
    x_on_time_rate = fields.Float('On-Time Delivery %', default=100.0)
    
    @api.depends('x_on_time_rate')
    def _compute_rating(self):
        for partner in self:
            rate = partner.x_on_time_rate
            if rate >= 95:
                partner.x_rating = 5.0
            elif rate >= 85:
                partner.x_rating = 4.5
            elif rate >= 75:
                partner.x_rating = 4.0
            elif rate >= 60:
                partner.x_rating = 3.0
            elif rate >= 40:
                partner.x_rating = 2.0
            else:
                partner.x_rating = 1.0