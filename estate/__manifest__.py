# -*- coding: utf-8 -*-

{
    "name": "estate",
    "description": "",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/estate-property/view.xml",
        "views/estate-property/actions.xml",
        "views/estate-property/menus.xml",

        "views/offer/view.xml",
        "views/offer/actions.xml",
        "views/offer/menus.xml",

        "views/tag/view.xml",
        "views/tag/actions.xml",
        "views/tag/menus.xml",

        "views/type/actions.xml",
        "views/type/view.xml",
        "views/type/menus.xml",

    ],
    "application": True,
    "installable": True,
}
