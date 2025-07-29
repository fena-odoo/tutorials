// awesome_owl/static/src/card/card.js
import { Component } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    // expected props and their types
    static props = {
        title: { type: String, optional: true },
        content: { type: String, optional: true },
      };
    
      // default values (used if props are missing)
      static defaultProps = {
        title: "Untitled Card",
        content: "No content provided",
      };
}
