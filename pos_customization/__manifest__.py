{
    'name': 'POS Customization',
    'version': '1.0',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # 'pos_customization/static/src/xml/orderline_template.xml',
            # 'pos_customization/static/src/xml/product_info_template.xml',
            # 'pos_customization/static/src/xml/receipt_template.xml',
            'pos_customization/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
