from odoo import models, fields, api

class VendorQuotation(models.Model):
    _name = 'vendorbridge.quotation'
    _description = 'Vendor Quotation Response'
    _inherit = ['mail.thread']
    _order = 'create_date desc'
    
    rfq_id = fields.Many2one('purchase.order', string='RFQ', required=True, ondelete='cascade')
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True,
        domain=[('x_is_vendor', '=', True)])
    line_ids = fields.One2many('vendorbridge.quotation.line', 'quotation_id', string='Quote Lines')
    total_amount = fields.Float('Total Amount', compute='_compute_total', store=True)
    delivery_days = fields.Integer('Delivery Days', default=7)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    attachment = fields.Binary('Quotation File')
    attachment_name = fields.Char('File Name')
    submitted_at = fields.Datetime('Submitted At')
    notes = fields.Text('Vendor Notes')
    
    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for quote in self:
            quote.total_amount = sum(line.subtotal for line in quote.line_ids)
    
    def action_submit(self):
        self.ensure_one()
        self.status = 'submitted'
        self.submitted_at = fields.Datetime.now()
        
        rfq = self.rfq_id
        if all(q.status == 'submitted' for q in rfq.quotation_ids) and rfq.x_status == 'sent':
            rfq.x_status = 'quoted'
        
        rfq.message_post(
            body='Quote received from %s (Rs.%s)' % (self.vendor_id.name, self.total_amount),
            message_type='notification',
            subtype_xmlid='mail.mt_activities'
        )
        return True

class VendorQuotationLine(models.Model):
    _name = 'vendorbridge.quotation.line'
    _description = 'Quotation Line Item'
    
    quotation_id = fields.Many2one('vendorbridge.quotation', required=True, ondelete='cascade')
    product_name = fields.Char('Item Name', required=True)
    quantity = fields.Float('Quantity', default=1.0)
    unit_price = fields.Float('Unit Price', default=0.0)
    subtotal = fields.Float('Subtotal', compute='_compute_subtotal', store=True)
    
    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price