from odoo import models, fields, api

class VendorBridgeActivityLog(models.Model):
    _name = 'vendorbridge.activity_log'
    _description = 'Activity Audit Log'
    _order = 'create_date desc'
    
    name = fields.Char('Action', required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    model_name = fields.Char('Model')
    record_id = fields.Integer('Record ID')
    action_type = fields.Selection([
        ('create', 'Create'),
        ('write', 'Update'),
        ('delete', 'Delete'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('generate', 'Generate'),
    ], string='Action Type')
    details = fields.Text('Details')
    ip_address = fields.Char('IP Address')
    
    @api.model
    def log_action(self, name, model_name, record_id, action_type, details=''):
        return self.create({
            'name': name,
            'model_name': model_name,
            'record_id': record_id,
            'action_type': action_type,
            'details': details,
        })