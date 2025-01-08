import { LitElement, html } from 'https://unpkg.com/lit@2.0.0/index.js?module';

class HomePage extends LitElement {
  render() {
    return html`
      <div class="bg-white p-6 rounded shadow">
        <h1 class="text-2xl font-bold">Home Page</h1>
        <p>Welcome to the home page!</p>
      </div>
    `;
  }
}

customElements.define('home-page', HomePage);
