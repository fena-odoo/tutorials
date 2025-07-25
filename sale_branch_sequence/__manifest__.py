{
    'name': 'Sale Branch Sequence',
    'version': '1.0',
    'depends': ['sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_branch_views.xml',
        'views/sale_order_inherit_views.xml',
    ],
    'installable': True,
}
