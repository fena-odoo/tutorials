// awesome_owl/static/src/card/card.js
import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        // title: { type: String, optional: true },
        // content: { type: String, optional: true },

        title:{
            type: String,
            optional: false,
        },
        slots: {
          type: Object,
          shape: {
            default: true,
          },
        },
      };

    setup() {
        this.state = useState({ isOpen: true });
    }

    toggleContent() {
        this.state.isOpen = !this.state.isOpen;
    }
    
      // default values (used if props are missing)
//       static defaultProps = {
//         title: "Untitled Card",
//         content: "No content provided",
//       };
}
