import { LitElement, html } from 'https://unpkg.com/lit@2.0.0/index.js?module';
import './home.js'; // Import home component
import './about.js'; // Import about component
import './contact.js'; // Import contact component

class MyApp extends LitElement {
  static get properties() {
    return {
      route: { type: String }
    };
  }

  constructor() {
    super();
    this.route = window.location.pathname;
    window.onpopstate = () => this.route = window.location.pathname;
  }

  navigate(event) {
    event.preventDefault();
    const href = event.target.getAttribute('href');
    history.pushState(null, '', href);
    this.route = href;
  }

  render() {
    return html`
      <header class="flex flex-wrap sm:justify-start sm:flex-nowrap w-full bg-white text-sm py-3">
        <nav class="max-w-[85rem] w-full mx-auto px-4 sm:flex sm:items-center sm:justify-between">
          <a class="flex-none font-semibold text-xl text-black focus:outline-none focus:opacity-80" href="/" @click="${this.navigate}" aria-label="Brand">My App</a>
          <div class="flex flex-row items-center gap-5 mt-5 sm:justify-end sm:mt-0 sm:ps-5">
            <a class="font-medium text-blue-500 focus:outline-none" href="/" @click="${this.navigate}" aria-current="${this.route === '/' ? 'page' : undefined}">Home</a>
            <a class="font-medium text-gray-600 hover:text-gray-400 focus:outline-none focus:text-gray-400" href="/about" @click="${this.navigate}">About</a>
            <a class="font-medium text-gray-600 hover:text-gray-400 focus:outline-none focus:text-gray-400" href="/contact" @click="${this.navigate}">Contact</a>
            <a class="font-medium text-gray-600 hover:text-gray-400 focus:outline-none focus:text-gray-400" href="#">Account</a>
            <a class="font-medium text-gray-600 hover:text-gray-400 focus:outline-none focus:text-gray-400" href="#">Work</a>
            <a class="font-medium text-gray-600 hover:text-gray-400 focus:outline-none focus:text-gray-400" href="#">Blog</a>
          </div>
        </nav>
      </header>

      <main class="p-6">
        ${this.route === '/' ? html`<home-page></home-page>` : ''}
        ${this.route === '/about' ? html`<about-page></about-page>` : ''}
        ${this.route === '/contact' ? html`<contact-page></contact-page>` : ''}
      </main>
    `;
  }
}

customElements.define('my-app', MyApp);
