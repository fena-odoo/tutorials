import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";
import { useAutofocus } from "@awesome_owl/utils";

export class TodoList extends Component {
  static template = "awesome_owl.TodoList";
  static components = { TodoItem };

  setup() {
    // this.todos = useState([
    //   { id: 1, description: "Buy milk", isCompleted: true },
    //   { id: 2, description: "Wash dishes", isCompleted: false },
    //   { id: 3, description: "Learn Owl.js", isCompleted: true },
    // ]);
    this.todos = useState([]);
    this.nextId = 1;
    // this.inputRef = useRef("todoInput"); // Reference to the input element
    // onMounted(() => {this.inputRef.el.focus();}); // Focus input on mount
    this.inputRef = useAutofocus("todoInput"); // Use custom hook for autofocus
  }

  addTodo(event) {
    // only act on Enter key (keyCode 13)
    if(event.keyCode === 13) {
      const description = event.target.value.trim();

      if (description) {
        this.todos.push({
          id: this.nextId++,
          description,
          isCompleted: false,
        });
        event.target.value = ""; // clear input
      }
    }
  }

  toggleTodo = (todoId) => {
    const todo = this.todos.find((t) => t.id === todoId);
    if (todo) {
      todo.isCompleted = !todo.isCompleted;
    }
  };

  removeTodo = (todoId) => {
    const index = this.todos.findIndex((t) => t.id === todoId);
    if (index >= 0) {
        this.todos.splice(index, 1);
    }
};

}
