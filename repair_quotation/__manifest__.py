
{
    'name': 'Repair Quotations',
    'version': '14.0.1.0.3',
    'category': 'Repair/Point of Sale',
    'sequence': 6,
    'license': 'LGPL-3',
    'summary': 'Create Quotation and Save Quotation from Repair module',
    'description': """
        repair_save_quotation,
        """,
    'author': "Shunkawakan Zubizarreta",
    'website': 'abtechsolution.in',
    'depends': ['point_of_sale','repair'],
    'data': [
        'views/assests.xml',
        'views/pos_quotation.xml',
    ],
    'qweb': [
        'static/src/xml/CreateQuotationButton.xml',
        'static/src/xml/SaveQuotationPopUp.xml',
    ],
    'installable': True,
}
