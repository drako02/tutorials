# -*- coding: utf-8 -*-

{
    'name': "estate",
    "description": '',
    'depends': [
        'base'
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/actions.xml',

    ],
    'application': True,
    'installable': True,
}