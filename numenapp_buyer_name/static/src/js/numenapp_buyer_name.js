odoo.define('numenapp_buyer_name.alias_button', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class AliasButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        is_available() {
            const order = this.env.pos.get_order();
            return order;
        }
        onClick() {
            const cli = this.get_client();
            alert(cli.name);
        }
    }
    AliasButton.template = 'AliasButton';

    ProductScreen.addControlButton({
        component: AliasButton,
        condition: function() {
            return this.env.pos;
        },
        position: ['before', 'OrderlineCustomerNoteButton'],
    });

    Registries.Component.add(AliasButton);

    return AliasButton;
});