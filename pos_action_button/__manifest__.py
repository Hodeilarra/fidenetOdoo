
{
    'name': 'CustomButton',
    'summary': '',
    "version": "14.0.1.0.0",

    'description': "Custom button in POS screen",
    'license': 'AGPL-3',
    'category': 'Point Of Sales',
    'depends': [
        'base', 'point_of_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
    'qweb': [
	    'static/src/xml/action_button.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}
