from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    x_rfq_title = fields.Char('RFQ Title', required=True)
    x_deadline = fields.Date('Quote Deadline')
    x_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Priority', default='medium')
    x_status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('quoted', 'Quotes Received'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('po_created', 'PO Created'),
        ('done', 'Done'),
    ], string='RFQ Status', default='draft', tracking=True)
    x_approval_notes = fields.Text('Approval Remarks')
    vendor_ids = fields.Many2many('res.partner', string='Invited Vendors',
        domain=[('x_is_vendor', '=', True), ('x_vendor_status', '=', 'active')])
    quotation_ids = fields.One2many('vendorbridge.quotation', 'rfq_id', string='Quotations')
    
    def action_send_rfq(self):
        self.ensure_one()
        if self.x_status != 'draft':
            raise UserError(_('RFQ must be in Draft state to send.'))
        
        self.x_status = 'sent'
        self.state = 'sent'
        
        for vendor in self.vendor_ids:
            self.env['vendorbridge.quotation'].create({
                'rfq_id': self.id,
                'vendor_id': vendor.id,
                'status': 'draft',
            })
        
        self.message_post(
            body=_('RFQ sent to %s vendors.') % len(self.vendor_ids),
            message_type='notification',
            subtype_xmlid='mail.mt_note'
        )
        return True
    
    def action_approve(self):
        self.ensure_one()
        if self.x_status not in ['review', 'quoted']:
            raise UserError(_('RFQ must be under review to approve.'))
        
        self.x_status = 'approved'
        self.state = 'purchase'
        
        if not self.name or self.name.startswith('RFQ'):
            self.name = self.env['ir.sequence'].next_by_code('purchase.order') or 'PO-2026-0001'
        
        self.action_create_invoice()
        self.x_status = 'po_created'
        
        self.message_post(
            body=_('RFQ approved by %s.') % self.env.user.name,
            message_type='notification',
            subtype_xmlid='mail.mt_activities'
        )
        return True
    
    def action_reject(self, notes=None):
        self.ensure_one()
        if self.x_status not in ['review', 'quoted']:
            raise UserError(_('RFQ must be under review to reject.'))
        
        self.x_status = 'rejected'
        self.x_approval_notes = notes or ''
        
        self.message_post(
            body=_('RFQ rejected. Reason: %s') % (notes or 'No reason provided'),
            message_type='notification',
            subtype_xmlid='mail.mt_activities'
        )
        return True
    
    def action_create_invoice(self):
        self.ensure_one()
        invoice_vals = {
            'move_type': 'in_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [],
        }
        for line in self.order_line:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                'name': line.name,
                'quantity': line.product_qty,
                'price_unit': line.price_unit,
                'tax_ids': [(6, 0, line.taxes_id.ids)],
            }))
        return self.env['account.move'].create(invoice_vals)
    
    @api.model
    def get_dashboard_data(self):
        return {
            'active_rfqs': self.search_count([('x_status', '=', 'sent')]),
            'pending_approvals': self.search_count([('x_status', 'in', ['quoted', 'review'])]),
            'total_spend_mtd': sum(self.search([
                ('state', '=', 'purchase'),
                ('date_order', '>=', fields.Date.today().replace(day=1))
            ]).mapped('amount_total')),
            'overdue_invoices': self.env['account.move'].search_count([
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('invoice_date_due', '<', fields.Date.today()),
                ('payment_state', '!=', 'paid')
            ]),
            'recent_activity': self._get_recent_activity(),
            'quick_actions': [
                {'label': '+ New RFQ', 'route': '/rfq/create'},
                {'label': '+ Add Vendor', 'route': '/vendor/add'},
                {'label': 'View Quotations', 'route': '/quotations'},
            ]
        }
    
    def _get_recent_activity(self, limit=5):
        messages = self.env['mail.message'].search([
            ('model', '=', 'purchase.order'),
        ], order='date desc', limit=limit)
        
        result = []
        for msg in messages:
            body = msg.body or ''
            subject = msg.subject or ''
            action = 'Action'
            if 'RFQ' in subject:
                action = 'RFQ Created'
            elif 'Quote' in body:
                action = 'Quote Received'
            elif 'approved' in body.lower():
                action = 'RFQ Approved'
            elif 'PO' in subject:
                action = 'PO Generated'
            
            result.append({
                'action': action,
                'user': msg.author_id.name if msg.author_id else 'System',
                'time': msg.date.strftime('%Y-%m-%d %H:%M:%S') if msg.date else '',
                'rfq_name': subject or 'Unknown',
            })
        return result
    
    def get_comparison_data(self):
        self.ensure_one()
        quotes = self.quotation_ids.filtered(lambda q: q.status == 'submitted')
        if not quotes:
            return {'error': 'No quotations submitted yet'}
        
        items = []
        for line in self.order_line:
            items.append({
                'name': line.name,
                'quantity': line.product_qty,
                'unit': line.product_uom.name if line.product_uom else 'Unit'
            })
        
        vendors = []
        for quote in quotes:
            vendor_data = {
                'vendor_id': quote.vendor_id.id,
                'vendor_name': quote.vendor_id.name,
                'vendor_rating': quote.vendor_id.x_rating,
                'total_amount': quote.total_amount,
                'delivery_days': quote.delivery_days,
                'lines': []
            }
            for line in quote.line_ids:
                vendor_data['lines'].append({
                    'item_name': line.product_name,
                    'quantity': line.quantity,
                    'unit_price': line.unit_price,
                    'subtotal': line.subtotal
                })
            vendors.append(vendor_data)
        
        cheapest = min(vendors, key=lambda v: v['total_amount'])
        ai_suggestion = {
            'recommended_vendor_id': cheapest['vendor_id'],
            'reason': 'Lowest total cost (Rs.{:,.2f})'.format(cheapest['total_amount']),
            'savings': ''
        }
        if len(vendors) > 1:
            next_best = sorted(vendors, key=lambda v: v['total_amount'])[1]
            savings = next_best['total_amount'] - cheapest['total_amount']
            pct = (savings / next_best['total_amount']) * 100
            ai_suggestion['savings'] = 'Rs.{:,.2f} ({:.1f}% cheaper)'.format(savings, pct)
        
        return {
            'rfq_title': self.x_rfq_title,
            'rfq_id': self.id,
            'items': items,
            'vendors': vendors,
            'ai_suggestion': ai_suggestion
        }
    
    @api.model
    def get_report_summary(self):
        return {
            'total_spend': sum(self.search([
                ('state', '=', 'purchase'),
                ('date_order', '>=', fields.Date.today().replace(day=1))
            ]).mapped('amount_total')),
            'active_vendors': self.env['res.partner'].search_count([
                ('x_is_vendor', '=', True),
                ('x_vendor_status', '=', 'active')
            ]),
            'po_fulfillment_rate': 94,
            'overdue_invoices': self.env['account.move'].search_count([
                ('move_type', '=', 'in_invoice'),
                ('state', '=', 'posted'),
                ('invoice_date_due', '<', fields.Date.today()),
                ('payment_state', '!=', 'paid')
            ])
        }
    
    @api.model
    def get_monthly_trend(self, months=6):
        from datetime import datetime, timedelta
        labels, data = [], []
        for i in range(months-1, -1, -1):
            month_date = datetime.now() - timedelta(days=i*30)
            month_start = month_date.replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            labels.append(month_start.strftime('%b'))
            data.append(sum(self.search([
                ('state', '=', 'purchase'),
                ('date_order', '>=', month_start.strftime('%Y-%m-%d')),
                ('date_order', '<=', month_end.strftime('%Y-%m-%d'))
            ]).mapped('amount_total')))
        return {'labels': labels, 'data': data}
    
    @api.model
    def get_category_breakdown(self):
        categories = ['it_hardware', 'office_supplies', 'furniture', 'logistics', 'stationery']
        labels = ['IT Hardware', 'Office Supplies', 'Furniture', 'Logistics', 'Stationery']
        data = []
        for cat in categories:
            vendors = self.env['res.partner'].search([('x_vendor_category', '=', cat)])
            data.append(sum(self.search([
                ('state', '=', 'purchase'),
                ('partner_id', 'in', vendors.ids)
            ]).mapped('amount_total')))
        return {'labels': labels, 'data': data}