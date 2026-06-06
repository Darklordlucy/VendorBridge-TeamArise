# -*- coding: utf-8 -*-
{
    'name': 'VendorBridge ERP',
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'summary': 'Procurement & Vendor Management ERP with AI features',
    'description': """
        Digitizes vendor management, RFQs, quotations, approvals, purchase orders, and invoices.
        Includes AI-powered Quote Reader, Voice-to-RFQ, and Procurement Copilot.
    """,
    'author': 'VendorBridge Hackathon Team',
    'depends': ['purchase', 'contacts', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/vendorbridge_security.xml',
        'views/vendor_views.xml',
        'views/rfq_views.xml',
        'views/dashboard_views.xml',
        'views/menu.xml',
        'data/demo_data.xml',
        'data/email_templates.xml',
        'reports/purchase_order.xml',
        'reports/invoice_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vendorbridge/static/src/css/vendorbridge.css',
            'vendorbridge/static/src/js/voice_to_rfq.js',
            'vendorbridge/static/src/js/chat_copilot.js',
            'vendorbridge/static/src/js/quote_reader.js',
        ],
        'web.assets_qweb': [
            'vendorbridge/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
