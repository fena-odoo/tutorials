/** @odoo-module **/

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook"; // gives access to the current POS

patch(Orderline.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    removeLine(ev) {
        ev.stopPropagation();

        const order = this.pos.get_order();
        const selectedLine = order?.get_selected_orderline();

        if (order && selectedLine) {
            order.removeOrderline(selectedLine);
        } else {
            console.warn("Could not find current order or selected orderline.", {
                order,
                selectedLine,
            });
        }
    },
});
