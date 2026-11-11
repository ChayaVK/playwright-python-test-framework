// Practice Shop: a small demo web app for the framework's tests. Data lives in localStorage.
const PRODUCTS = [
  { slug: 'laptop-bag', name: 'Laptop Bag', price: 49.99, desc: 'Padded bag for laptops up to 15 inches.' },
  { slug: 'wireless-mouse', name: 'Wireless Mouse', price: 19.99, desc: 'Quiet clicks, 12 months of battery.' },
  { slug: 'usb-c-cable', name: 'USB-C Cable', price: 9.99, desc: 'Braided, 2 meters, fast charging.' },
  { slug: 'bluetooth-speaker', name: 'Bluetooth Speaker', price: 39.99, desc: 'Waterproof speaker with deep bass.' },
  { slug: 'water-bottle', name: 'Water Bottle', price: 14.99, desc: 'Keeps drinks cold for 24 hours.' },
  { slug: 'desk-lamp', name: 'Desk Lamp', price: 24.99, desc: 'LED lamp with three brightness levels.' }
];
const USERS = { standard_user: 'Test@123', locked_user: 'Test@123' };
const TAX_RATE = 0.08;

const cart = () => JSON.parse(localStorage.getItem('cart') || '[]');
const saveCart = items => localStorage.setItem('cart', JSON.stringify(items));
const money = n => '$' + n.toFixed(2);
const bySlug = slug => PRODUCTS.find(p => p.slug === slug);

function requireLogin() {
  if (!localStorage.getItem('user')) {
    sessionStorage.setItem('loginError', 'You must log in to view this page');
    location.href = 'index.html';
  }
}

function header(title) {
  const count = cart().length;
  document.body.insertAdjacentHTML('afterbegin',
    `<header><span class="app-title">${title}</span><nav>
       <a id="products-link" href="products.html">Products</a>
       <a id="cart-link" href="cart.html">Cart${count ? `<span id="cart-badge" class="badge">${count}</span>` : ''}</a>
       <a id="practice-link" href="practice.html">Practice</a>
       <a id="logout-link" href="#">Logout</a></nav></header>`);
  document.getElementById('logout-link').onclick = e => {
    e.preventDefault(); localStorage.clear(); location.href = 'index.html';
  };
}

function showError(msg) {
  const el = document.querySelector('[data-test="error"]');
  el.textContent = msg; el.classList.remove('hidden');
}
