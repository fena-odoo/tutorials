/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    getReceiptHeaderData(order) {
        const data = super.getReceiptHeaderData(order);
        return {
            ...data,
            congratulatoryText: this.config.congratulatory_text || "Arigato Gozaimasu!",
        }
    }
});