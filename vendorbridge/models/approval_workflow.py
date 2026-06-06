from odoo import models, fields, api

class VendorBridgeApproval(models.Model):
    _name = 'vendorbridge.approval'
    _description = 'Approval Workflow Record'
    _inherit = ['mail.thread']
    _order = 'create_date desc'
    
    rfq_id = fields.Many2one('purchase.order', string='RFQ', required=True)
    approver_id = fields.Many2one('res.users', string='Approver')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delegated', 'Delegated'),
    ], string='Status', default='pending', tracking=True)
    notes = fields.Text('Approval Notes')
    delegated_to = fields.Many2one('res.users', string='Delegated To')
    approved_at = fields.Datetime('Approved At')
    
    def action_approve(self):
        self.ensure_one()
        self.state = 'approved'
        self.approved_at = fields.Datetime.now()
        self.rfq_id.action_approve()
    
    def action_reject(self, notes):
        self.ensure_one()
        self.state = 'rejected'
        self.notes = notes
        self.rfq_id.action_reject(notes)
    
    def action_delegate(self, user_id):
        self.ensure_one()
        self.state = 'delegated'
        self.delegated_to = user_id