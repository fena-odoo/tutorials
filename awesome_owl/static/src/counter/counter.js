// awesome_owl/static/src/counter/counter.js
import { Component, useState } from "@odoo/owl";

export class Counter extends Component {
    static template = "awesome_owl.Counter";

    static props = {
        onChange: { type: Function, optional: true },  // Accept optional callback
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        // Call the parent's callback if defined
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}
