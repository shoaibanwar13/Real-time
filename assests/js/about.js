import { LitElement, html } from 'https://unpkg.com/lit@2.0.0/index.js?module';

class AboutPage extends LitElement {
  render() {
    return html`
      <div class="bg-white p-6 rounded shadow">
        <h1 class="text-2xl font-bold">About Page</h1>
        <p>This is the about page!</p>
      </div>
    `;
  }
}

customElements.define('about-page', AboutPage);
