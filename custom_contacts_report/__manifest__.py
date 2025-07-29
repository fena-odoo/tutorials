{
    'name': 'Custom Contacts Report',
    'version': '1.0',
    'summary': 'PDF report showing selected contacts with name and email',
    'description': """
        This module provides a custom PDF report that lists selected contacts (res.partner) 
        with their names and email addresses.
    """,
    'depends': ['base', 'contacts'],
    'data': [
        'report/contact_report_template.xml',
        'report/contact_report_actions.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
