odoo.define ('categories_pos.CategoryButton', function (require) { 
    'use strict'; 
    const PosComponent = require ('point_of_sale.PosComponent'); 
    const ProductScreen = require ('point_of_sale.ProductScreen'); 
    const {useListener} = require ('web.custom_hooks'); 
    const Registries = require ('point_of_sale.Registries'); 
    class CategoryButton extends PosComponent { 
    } 
    CategoryButton.template = 'ProductCategoryWidget'; 
    ProductScreen.addControlButton ({ 
        component: CategoryButton, 
        condition: function () { 
            return true; 
        }, 
        position: ['before', 'SetPricelistButton'],
    });
    Registries.Component.add (CategoryButton); 
    return CategoryButton; 
 });

 ProductScreen.addControlButton ({ 
    component: CategoryButton, 
    condition: function () { 
        return true; 
    }, 
    position: ['before', 'SetPricelistButton'], 
});