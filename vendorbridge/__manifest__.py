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
        'security/vendorbridge_security.xml',
        'security/ir.model.access.csv',
        'data/demo_data.xml',
        'reports/email_templates.xml',
        'views/vendor_views.xml',
        'views/rfq_views.xml',
        'views/quotation_views.xml',
        'views/approval_views.xml',
        'views/activity_log_views.xml',
        'views/dashboard_views.xml',
        'views/menu.xml',
        'reports/purchase_order.xml',
        'reports/invoice_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}