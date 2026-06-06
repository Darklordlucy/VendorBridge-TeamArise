import requests
import base64
import json
import re
from odoo import http, fields
from odoo.http import request

class AIServices(http.Controller):
    
    # ============ SMART QUOTE READER (Gemini API) ============
    
    @http.route("/vendorbridge/extract_quote", type="json", auth="public", methods=["POST"], csrf=False)
    def extract_quote(self, file_data=None, file_name=None, **kw):
        if not file_data:
            return {'success': False, 'error': 'No file provided'}
        
        try:
            api_key = request.env['ir.config_parameter'].sudo().get_param(
                'vendorbridge.gemini_api_key', 'YOUR_GEMINI_API_KEY')
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            mime_type = "application/pdf" if file_name and file_name.endswith(".pdf") else "image/jpeg"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "Extract from this quotation and return ONLY JSON: {items: [{name, quantity, unit_price, total}], delivery_date, vendor_name, total_amount, tax_rate}"},
                        {"inline_data": {"mime_type": mime_type, "data": file_data}}
                    ]
                }]
            }
            
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
            result = response.json()
            
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            text = text.replace("```json", "").replace("```", "").strip()
            
            return {'success': True, 'result': json.loads(text)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ============ VOICE-TO-RFQ ============
    
    @http.route("/vendorbridge/voice_to_rfq", type="json", auth="user", methods=["POST"])
    def voice_to_rfq(self, transcript=None, **kw):
        if not transcript:
            return {'success': False, 'error': 'No transcript provided'}
        
        text = transcript.lower()
        
        # Extract quantity
        qty_match = re.search(r'(\d+)\s*(laptops?|chairs?|desks?|units?|pcs?)', text)
        quantity = int(qty_match.group(1)) if qty_match else 1
        
        # Extract item name
        items_map = {
            'laptop': 'Laptop', 'chair': 'Chair', 'desk': 'Desk',
            'monitor': 'Monitor', 'keyboard': 'Keyboard', 'mouse': 'Mouse', 'printer': 'Printer'
        }
        item_name = 'Item'
        for key, val in items_map.items():
            if key in text:
                item_name = val
                break
        
        # Extract deadline
        deadline = None
        if 'tomorrow' in text:
            from datetime import datetime, timedelta
            deadline = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif 'next week' in text:
            from datetime import datetime, timedelta
            deadline = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        elif 'next month' in text:
            from datetime import datetime, timedelta
            deadline = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        return {
            'success': True,
            'result': {
                'title': transcript[:50],
                'deadline': deadline,
                'priority': 'medium',
                'items': [{'name': item_name, 'quantity': quantity, 'unit': 'pieces'}],
                'vendors': []
            }
        }
    
    # ============ PROCUREMENT COPILOT (Groq API) ============
    
    @http.route("/vendorbridge/copilot", type="json", auth="user", methods=["POST"])
    def procurement_copilot(self, question=None, **kw):
        if not question:
            return {'type': 'text', 'message': 'Please ask a question.'}
        
        q = question.lower()
        
        # Intent 1: Pending approvals
        if any(w in q for w in ["pending", "approval", "approve"]):
            pending = request.env['vendorbridge.approval'].search_count([("state", "=", "pending")])
            return {'type': 'text', 'message': f"You have {pending} pending approvals."}
        
        # Intent 2: Total spending
        if any(w in q for w in ["spend", "spent", "total", "amount"]):
            pos = request.env['purchase.order'].search([("state", "=", "purchase")])
            total = sum(po.amount_total for po in pos)
            return {'type': 'text', 'message': f"Total spending: Rs.{total:,.2f}"}
        
        # Intent 3: Vendor count
        if any(w in q for w in ["vendor", "supplier", "how many vendors"]):
            count = request.env['res.partner'].search_count([('x_is_vendor', '=', True)])
            return {'type': 'text', 'message': f"You have {count} registered vendors."}
        
        # Intent 4: Lowest quote
        if any(w in q for w in ["cheapest", "lowest", "best price"]):
            rfq = request.env['purchase.order'].search([], order="create_date desc", limit=1)
            if rfq and rfq.quotation_ids:
                quotes = rfq.quotation_ids.filtered(lambda q: q.status == 'submitted')
                if quotes:
                    lowest = min(quotes, key=lambda q: q.total_amount)
                    return {'type': 'text', 'message': f"Lowest: Rs.{lowest.total_amount:,.2f} from {lowest.vendor_id.name}"}
            return {'type': 'text', 'message': "No quotes found."}
        
        # Intent 5: IT hardware spending
        if any(w in q for w in ["it hardware", "computer", "laptop"]):
            vendors = request.env['res.partner'].search([('x_vendor_category', '=', 'it_hardware')])
            pos = request.env['purchase.order'].search([('state', '=', 'purchase'), ('partner_id', 'in', vendors.ids)])
            total = sum(po.amount_total for po in pos)
            return {'type': 'text', 'message': f"IT hardware spending: Rs.{total:,.2f}"}
        
        # Fallback: Groq LLM
        try:
            groq_key = request.env['ir.config_parameter'].sudo().get_param('vendorbridge.groq_api_key', '')
            if not groq_key:
                return {'type': 'text', 'message': "Try: 'pending approvals', 'total spend', 'top vendors'"}
            
            url = "https://api.groq.com/openai/v1/chat/completions"
            vc = request.env['res.partner'].search_count([('x_is_vendor', '=', True)])
            pc = request.env['vendorbridge.approval'].search_count([("state", "=", "pending")])
            context = f"{vc} vendors, {pc} pending approvals."
            
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": f"You are VendorBridge AI. Brief answers. Context: {context}"},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.3,
                "max_tokens": 150
            }
            
            response = requests.post(url, json=payload,
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}, timeout=10)
            result = response.json()
            
            return {'type': 'text', 'message': result["choices"][0]["message"]["content"]}
            
        except:
            return {'type': 'text', 'message': "Try: 'pending approvals', 'total spend', 'top vendors'"}