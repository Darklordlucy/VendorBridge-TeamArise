{
    'name': 'VendorBridge',
    'version': '1.0',
    'category': 'Operations/Purchase',
    'summary': 'Procurement & Vendor Management ERP',
    'description': """
        VendorBridge digitizes the entire procurement lifecycle.
    """,
    'author': 'VendorBridge Team',
    'depends': ['base', 'purchase', 'account', 'mail', 'website', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'security/vendorbridge_security.xml',
        'data/demo_data.xml',
        'data/email_templates.xml',
        'views/vendor_views.xml',
        'views/rfq_views.xml',
        'views/dashboard_views.xml',
        'views/menu.xml',
        'reports/purchase_order.xml',
        'reports/invoice_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}