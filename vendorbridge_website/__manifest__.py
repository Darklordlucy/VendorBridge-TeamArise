<<<<<<< HEAD
# -*- coding: utf-8 -*-
{
    'name': 'VendorBridge Portal',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Vendor portal for RFQ submissions and quotation comparison',
    'description': """
        Public/magic-link portals for vendors to view RFQs, upload quotes via Gemini AI reader,
        and track purchase order statuses.
    """,
    'author': 'VendorBridge Hackathon Team',
    'depends': ['website', 'vendorbridge'],
=======
{
    'name': 'VendorBridge Website Portal',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Vendor-facing portal for VendorBridge',
    'depends': ['vendorbridge', 'website', 'portal'],
>>>>>>> origin/feat/backend
    'data': [
        'views/vendor_portal.xml',
        'views/rfq_list.xml',
        'views/comparison_page.xml',
    ],
<<<<<<< HEAD
    'assets': {
        'web.assets_frontend': [
            'vendorbridge_website/static/css/portal.css',
            'vendorbridge_website/static/js/portal.js',
            'vendorbridge_website/static/js/chart_config.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
=======
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
>>>>>>> origin/feat/backend
