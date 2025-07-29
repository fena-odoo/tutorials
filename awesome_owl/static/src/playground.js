// awesome_owl/static/src/playground.js
import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";  // Import the sub-component
import { Card } from "./card/card";
import { TodoList } from "./todo_list/todo_list";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList };  // Register Counter as a child component

    setup() {
        this.htmlContent = markup("<strong>This is bold HTML</strong>");
        this.plainText = "<script>alert('XSS');</script>"; // this will be escaped

        // Track each counter A and counter B value separately
        this.state = useState({ a: 0, b: 0 });
    }

    // Callback for counter A
    updateA(newValue) {
        this.state.a = newValue;
    }

    // Callback for counter B
    updateB(newValue) {
        this.state.b = newValue;
    }

    // Computed total sum
    get total() {
        return this.state.a + this.state.b;
    }
}
