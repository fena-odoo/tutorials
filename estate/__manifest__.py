{
    'name': 'Estate',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        "data/master_property_types.xml",
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'demo': [
        "demo/demo_property_data.xml",
    ],
}
