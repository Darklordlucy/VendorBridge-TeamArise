{
    'name': 'VendorBridge Website Portal',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Vendor-facing portal for VendorBridge',
    'depends': ['vendorbridge', 'website', 'portal'],
    'data': [
        'views/vendor_portal.xml',
        'views/rfq_list.xml',
        'views/comparison_page.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}