{
    'name': 'Sales Data Access',
    'version': '1.0',
    'depends': ['base', 'sale', 'sales_team'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
