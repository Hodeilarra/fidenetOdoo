odoo.define('clear_button_fun.pos_view',function(require){
    "use strict";
    
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    
    var ClearCartLine = screens.ActionButtonWidget.extend({
        template: "ClearCartLine",
    
        button_click: function(){
        var self = this;
        this.clear_button_fun();
        },
    
        clear_button_fun(){
        var order = this.pos.get_order();
        order.remove_orderline(order.get_selected_orderline())
        },
    });
    screens.define_action_button({
        'name': 'clear_button_fun',
        'widget': ClearCartLine,
    });
    });