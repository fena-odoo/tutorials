{
    'name': 'Estate',
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        # "data/master_property_types.xml",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        'report/estate_user_property_report.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'demo': [
        "demo/estate_demo.xml"
        # "demo/demo_property_data.xml",
    ],
}
