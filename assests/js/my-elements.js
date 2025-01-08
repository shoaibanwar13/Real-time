import { LitElement, html, css } from 'lit';

class MyComponent extends LitElement {
  static styles = css`
    button {
      background-color: blue;
      color: white;
      padding: 10px;
      border: none;
      border-radius: 5px;
    }
  `;

  constructor() {
    super();
    this.counter = 0;
  }

  render() {
    return html`
      <div>
        <h1>Counter: ${this.counter}</h1>
        <button @click="${this.increment}">Increment Counter</button>
      </div>
    `;
  }

  increment() {
    this.counter += 1;
  }
}

customElements.define('my-component', MyComponent);
