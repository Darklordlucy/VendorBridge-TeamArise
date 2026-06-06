from odoo import http, fields
from odoo.http import request

class VendorPortal(http.Controller):
    
    # ============ VENDOR PORTAL DATA ============
    
    @http.route("/vendorbridge/portal/rfq_data", type="json", auth="public", methods=["POST"], csrf=False)
    def portal_rfq_data(self, token=None, **kw):
        if not token:
            return {'success': False, 'error': 'No token provided'}
        
        try:
            rfq_id, vendor_id = map(int, token.split('-'))
            rfq = request.env['purchase.order'].sudo().browse(rfq_id)
            vendor = request.env['res.partner'].sudo().browse(vendor_id)
            
            if vendor not in rfq.vendor_ids:
                return {'success': False, 'error': 'Not invited to this RFQ'}
            
            if rfq.x_deadline and rfq.x_deadline < fields.Date.today():
                return {'success': False, 'error': 'Deadline has passed'}
            
            items = []
            for line in rfq.order_line:
                items.append({
                    'name': line.name,
                    'quantity': line.product_qty,
                    'unit': line.product_uom.name if line.product_uom else 'Unit',
                    'specifications': ''
                })
            
            return {
                'success': True,
                'result': {
                    'rfq_title': rfq.x_rfq_title,
                    'deadline': str(rfq.x_deadline) if rfq.x_deadline else None,
                    'items': items,
                    'vendor_name': vendor.name,
                    'token': token
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ============ SUBMIT QUOTATION ============
    
    @http.route("/vendorbridge/portal/submit_quote", type="json", auth="public", methods=["POST"], csrf=False)
    def portal_submit_quote(self, token=None, lines=None, delivery_days=None, total_amount=None, **kw):
        if not token or not lines:
            return {'success': False, 'error': 'Missing required fields'}
        
        try:
            rfq_id, vendor_id = map(int, token.split('-'))
            
            quotation = request.env['vendorbridge.quotation'].sudo().search([
                ('rfq_id', '=', rfq_id),
                ('vendor_id', '=', vendor_id)
            ], limit=1)
            
            if not quotation:
                quotation = request.env['vendorbridge.quotation'].sudo().create({
                    'rfq_id': rfq_id,
                    'vendor_id': vendor_id,
                })
            
            line_vals = []
            for line in lines:
                line_vals.append((0, 0, {
                    'product_name': line.get('product_name', ''),
                    'quantity': line.get('quantity', 0),
                    'unit_price': line.get('unit_price', 0),
                }))
            
            quotation.sudo().write({
                'line_ids': line_vals,
                'delivery_days': delivery_days or 7,
                'status': 'submitted',
                'submitted_at': fields.Datetime.now(),
            })
            
            return {'success': True, 'result': {'message': 'Quotation submitted successfully'}}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ============ VENDOR PORTAL PAGE (Website) ============
    
    @http.route("/vendor/quote/<string:token>", type="http", auth="public", website=True)
    def vendor_quote_page(self, token, **kw):
        try:
            rfq_id, vendor_id = map(int, token.split('-'))
            rfq = request.env['purchase.order'].sudo().browse(rfq_id)
            vendor = request.env['res.partner'].sudo().browse(vendor_id)
            
            if vendor not in rfq.vendor_ids:
                return request.render('vendorbridge_website.error_page', {'error': 'Not invited'})
            
            return request.render('vendorbridge_website.vendor_quote_template', {
                'rfq': rfq,
                'vendor': vendor,
                'token': token
            })
            
        except:
            return request.render('vendorbridge_website.error_page', {'error': 'Invalid link'})