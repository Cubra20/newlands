/* ==========================================================================
   NEWLAND'S CAFE: script.js
   Hi teammates! This is the ONE JavaScript file of our whole website. We only used HTML, CSS and JavaScript (no Python).
   This is our first time building a website system, so I wrote the comments in simple words to help us understand the code.

   HOW THE WHOLE SYSTEM WORKS (short version)
   - The website has 5 pages (index, menu, story, contact, manage) and every page loads this same file.
   - Each page only uses its own part. The "render" functions check first if their part is on the page. If not, they just stop.
   - The HTML pages are mostly empty boxes with ids. JavaScript fills them with the menu, the cart, the orders and so on.
   - We don't have a database. Everything (menu, stock, orders, messages) is saved in the browser with localStorage,
     so it stays in that browser on that computer only.

   HOW TO READ THE COMMENTS
   TASK = what the function must do
   HOW = a simple way to do it
   IN THE SYSTEM = where the function is used and why we need it

   WHAT'S ON THERE
   1. SHARED        helpers, settings, menu data, saved data, pictures, My Order drawer, buttons
   2. HOME PAGE     index.html
   3. MENU PAGE     menu.html
   4. STORY PAGE    story.html   (text only, no code needed)
   5. CONTACT PAGE  contact.html
   6. MANAGE PAGE   manage.html  (PIN gate, tabs, orders, menu + stock, edit window, messages)
   7. START         runs once when any page opens
   ========================================================================== */


/* ==========================================================================
   1. SHARED (used by every page)
   ========================================================================== */

/* ---- 1.1 Small helpers: tiny functions we use everywhere so we don't repeat long code ---- */
const $ = s => document.querySelector(s);   // shortcut for document.querySelector: $('#items') finds the element with id="items"
const on = (sel, ev, fn) => { const el = $(sel); if (el) el.addEventListener(ev, fn); };   // like addEventListener, but it does nothing if that element is not on this page (each page has different things)
const peso = n => '₱' + n.toLocaleString();
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));   // turns < > & " into safe text so what users type can't break the page (we need this because we use innerHTML)
const page = document.body.dataset.page;   // which page we are on: 'home', 'menu', 'story', 'contact' or 'manage' (it comes from <body data-page="...">)

/* TASK: Read and write saved data (menu, stock, orders, cart).
   HOW: localStorage can only keep TEXT, so write() turns our data into text with JSON.stringify and read() turns it back with JSON.parse.
        try/catch is there so the page doesn't crash if the browser blocks the storage or it is full.
   IN THE SYSTEM: this is our "database". The saved data (S), the cart and the other saving code all go through these two small functions. */
const read = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch (e) { return fallback; } };
const write = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch (e) { return false; } };

/* ---- 1.2 Settings and the starting menu: the names and data we use in the whole program ---- */
const KEY = 'newlands-v1', CART_KEY = 'newlands-cart';   // the names (keys) used to save things in localStorage: KEY = menu/orders/messages, CART_KEY = My Order
const LOGO = 'images/logo.png.png';   // the shop logo: shown when an item has no picture (check the file name in the images folder)
const EXTS = ['jpg', 'png', 'jpeg', 'webp'];   // the picture file types we try for each item

// CATS = the categories, in the same order as the tabs on the Menu page.
//   folder = the name of the group folder inside images/ (change it if your folder name is different)
//   sizes = cup sizes (only hot drinks)    add = add-ons as [name, price]
const CATS = {
  hot:    {folder:'hot collections',    label:'Hot',    sizes:['8oz','12oz'], add:[['Extra Espresso',40]]},
  iced:   {folder:'iced collections',   label:'Iced',   add:[['Upsize',25],['Extra Espresso',40]]},
  frappe: {folder:'frappe collections', label:'Frappe', add:[['Upsize',25]]},
  fizz:   {folder:'fizz collections',   label:'Fizz',   add:[['Upsize',10],['Sinkers',20]]},
  brewed: {folder:'brewed collections', label:'Brewed', add:[]},
  meals:  {folder:'meal collections',   label:'Meals',  add:[['Extra Rice',25],['Extra Egg',20]]}
};
// MENU = the starting menu from the Newland's menu PDF. Each item is [name, price] or, for hot drinks, [name, 8oz price, 12oz price].
const MENU = {
  meals:[['Soy Garlic Chicken',159],['Breaded Porkchop',179],['Boneless Bangus',169],['Tocilog',149],['Hotsilog',139],['Longsilog',149],['Corned Beef Silog',149],['Fried Pork Belly',179],['Fried Pork Chop',179]],
  iced:[['Iced Americano',80],['Iced Spanish Latte',125],['Iced Matcha Latte',125],['Iced Vanilla Latte',125],['Iced Caramel Macchiato',125],['Iced Cappuccino',125],['Iced Strawberry Matcha',150],['Iced Mocha Latte',125],['Iced Hazelnut Latte',125],['Iced Salted Caramel Latte',125],['Iced Chocolate Latte',125]],
  frappe:[['Strawberry Frappe',150],['Blueberry Frappe',150],['Matcha Frappe',150],['Mocha Frappe',150],['Caramel / Salted Frappe',150],['Coffee Jelly Frappe',150],['Java Chip Frappe',150],['Cookies and Cream Frappe',150],['Green Apple Frappe',150]],
  fizz:[['Strawberry Fizz',120],['Blueberry Fizz',120],['Green Apple Fizz',120],['Mango Fizz',120],['Blue Curacao Fizz',120],['Lemon Fizz',120],['Passion Fruit Fizz',120],['Sparkling Americano Fizz',120]],
  hot:[['Latte',80,100],['Americano',60,80],['Matcha Latte',100,120],['Cappuccino',80,100],['Spanish Latte',100,120],['Chocolate Latte',100,120],['Caramel Macchiato',100,120],['Vanilla Latte',100,120],['Herbal Tea',50,70]],
  brewed:[['French Press',120],['Chemex Pour Over',150],['Siphon Brewer',200],['V60 Dripper',150]]
};

/* ---- 1.3 Saved data: S is our "database" in memory, and save() writes it to the browser ---- */
let S = read(KEY, null) || seed();   // S = everything we save: items, orders, msgs and counters. Load it from the browser, or make the starting menu with seed() the first time
S.items.forEach(i => { if (i.img) i.img = i.img.startsWith('data:') ? '' : i.img.split('/').pop(); });   // clean-up for old saved data: an old version saved a whole path or photo here, now we only keep the file name
let cart = [], tt;   // cart = the lines in My Order, each {id, size, add:[add-on numbers], qty}. tt = timer id for the toast

/* TASK: Make the starting menu (all the items from the Newland's menu PDF) with stock.
   HOW: Loop over MENU (above). For each item make an object {id, cat, name, p (prices), stock: 20, img: ''} and put it in the items list. Each item gets its own id.
   IN THE SYSTEM: runs the first time a browser opens the website (nothing saved yet) and when the staff press "Reset all data" in Manage. */
function seed() {
  let id = 1; const items = [];
  for (const c in MENU) MENU[c].forEach(([name, ...p]) => items.push({id: id++, cat: c, name, p, stock: 20, img: ''}));
  return {items, orders: [], msgs: [], nextId: id, nextOrder: 1};
}
// TASK: Write S (all our data) to the browser. Used by commit() and by the Contact form. If it fails (storage full), tell the user.
function save() { if (!write(KEY, S)) toast('Could not save. The browser storage may be full.'); }
// TASK: Find an item by its id. We use ids (not names) everywhere because the name can be changed in Edit.
const item = id => S.items.find(i => i.id === id);

/* TASK: Check if an item matches the text typed in a search box.
   HOW: Join the item's name + category name, make it lowercase, then check if it includes the typed text (also lowercase). An empty box matches everything.
   IN THE SYSTEM: used by the search box on the Menu page (renderMenu) and the one above the table in Manage (renderInventory). */
const matches = (it, q) => (it.name + ' ' + CATS[it.cat].label).toLowerCase().includes(q.trim().toLowerCase());

/* TASK: Redraw the screen after something changed (refresh), or save the data and then redraw (commit).
   HOW: refresh() just calls every render function. Each one stops by itself if its part is not on this page, so it is safe on any page.
        commit() = save() + refresh(). Our rule: after changing S (the saved data), call commit().
   IN THE SYSTEM: called after almost every button: place order, mark as served, edit stock, add/remove item, reset data. */
function refresh() { renderHero(); renderMenu(); renderCart(); renderManage(); }
function commit() { save(); refresh(); }

/* TASK: Show a small message at the bottom of the screen (like "Order #3 placed").
   HOW: Put the text in the #toast box, show it, and hide it again after 2.5 seconds with setTimeout.
   IN THE SYSTEM: gives feedback to the customer and the staff after buttons (order placed, item added, saved, errors). */
function toast(msg) { const t = $('#toast'); t.textContent = msg; t.style.display = 'block'; clearTimeout(tt); tt = setTimeout(() => t.style.display = 'none', 2500); }

/* ---- 1.4 Item pictures: finds the picture of each item in the images folder (menu cards, Manage table, preview) ---- */
/* TASK: Find the picture file of an item inside the images folder.
   HOW: picList() makes a list of file paths to try, best guess first: the file name typed in Edit, then the item name ("iced matcha latte"),
        then the name without the last word latte/frappe/fizz ("iced matcha"). Every name is tried as .jpg, .png, .jpeg and .webp.
        Windows can hide the extension, so "latte.jpg" may really be "latte.jpg.jpg". That is why we try both.
        If a file is missing, the <img> calls nextPic() (onerror) and it tries the next path. If nothing works, it shows the logo.
   IN THE SYSTEM: the menu cards, the pictures in the Manage table and the preview in the Add/Edit window all use this. */
function picList(it) {
  const dir = 'images/' + CATS[it.cat].folder + '/', full = it.name.toLowerCase().trim();
  const names = [...new Set([(it.img || '').trim(), full, full.replace(/ (latte|frappe|fizz)$/, '')].filter(Boolean))];
  return names.flatMap(n => {
    const ext = n.match(/\.([a-z0-9]{3,4})$/i);
    return ext ? [n, n + '.' + ext[1]] : EXTS.flatMap(x => [n + '.' + x, n + '.' + x + '.' + x]);
  }).map(f => encodeURI(dir + f));
}
// TASK: Make the <img> text for an item's picture. onerror="nextPic(this)" means: if the file is missing, try the next path.
// IN THE SYSTEM: used by the menu cards (renderMenu) and the pictures in the Manage table (renderInventory).
const picTag = (it, cls = '') => `<img class="${cls}" src="${esc(picList(it)[0])}" data-id="${it.id}" data-n="0" alt="${esc(it.name)}" onerror="nextPic(this)">`;
// TASK: The browser calls this when a picture file is not found. Try the next path in the list; if none is left, show the logo.
function nextPic(im) {
  const list = im._list || picList(item(+im.dataset.id)), n = +im.dataset.n + 1;   // _list is only set by the preview in the Add/Edit window; the cards use picList() with the item id
  if (n < list.length) { im.dataset.n = n; im.src = list[n]; }
  else { im.onerror = null; im.src = LOGO; im.classList.add('def'); }
}

/* ---- 1.5 My Order: the drawer that opens from the "My Order" button on every page ---- */
// TASK: How many of this item are already in My Order (all sizes and add-ons together). Used so nobody can order more than the stock.
const inCart = id => cart.filter(l => l.id === id).reduce((s, l) => s + l.qty, 0);
// TASK: Get the size + add-on names of a cart line, like ["12oz", "Extra Espresso"].
// IN THE SYSTEM: shows the line in My Order and writes the order text when placing the order.
function lineOpts(l) { const c = CATS[item(l.id).cat]; return [c.sizes ? c.sizes[l.size] : '', ...l.add.map(a => c.add[a][0])].filter(Boolean); }

/* TASK: Compute the price of ONE cart line (unit) and of the WHOLE cart (cartTotal).
   HOW: Look up the item, take its price for the chosen size (p[size]), then add the price of each add-on that was ticked. Total = unit price × qty, added up for all lines.
   IN THE SYSTEM: used by My Order (to show the prices and the Total) and by placeOrder (to save the total of the order). */
function unit(l) { const it = item(l.id); return it.p[l.size] + l.add.reduce((s, a) => s + CATS[it.cat].add[a][1], 0); }
const cartTotal = () => cart.reduce((s, l) => s + unit(l) * l.qty, 0);

/* TASK: Add the parts that every page shares (the My Order drawer and the small message box), so we don't copy-paste them in 5 HTML files.
   HOW: insertAdjacentHTML puts this text as real HTML at the end of <body>.
   IN THE SYSTEM: runs once at START on every page, so the "My Order" button in the top bar always has a drawer to open. */
function mountShell() {
  document.body.insertAdjacentHTML('beforeend', `<div id="scrim" data-act="drawer"></div>
  <aside id="drawer" aria-label="My order"><div class="dh"><h3>My Order</h3><button class="ghost" data-act="drawer">Close</button></div><div id="cart"></div>
  <label for="cname">Name or table</label><input id="cname" maxlength="30" placeholder="Walk-in">
  <div class="total"><span>Total</span><span id="ctotal"></span></div><button class="pill dark wide" data-act="place">Place order</button></aside>
  <div id="toast" role="status"></div>`);
}

/* TASK: Draw My Order: every line with its options and the +/− buttons, the Total, and the small number on the "My Order" button. Also save the cart.
   HOW: Loop over cart with map() and build one row per line (data-i = the position of the line, so the +/− buttons know which line to change).
        write() saves the cart, so it is still there when the customer goes to another page.
   IN THE SYSTEM: called by refresh() every time the cart changes (add to order, +/−, place order). */
function renderCart() {
  $('#cart').innerHTML = cart.map((l, i) => `<div class="line"><div>${esc(item(l.id).name)}<small>${lineOpts(l).join(', ') || 'Plain'} · ${peso(unit(l))}</small></div>
    <div class="qty"><button data-act="dec" data-i="${i}" aria-label="Fewer">−</button>${l.qty}<button data-act="inc" data-i="${i}" aria-label="More">+</button></div></div>`).join('')
    || '<p><small>Your order is empty. Pick something from the menu.</small></p>';
  $('#ctotal').textContent = peso(cartTotal());
  $('#count').textContent = cart.reduce((s, l) => s + l.qty, 0);
  write(CART_KEY, cart);
}

/* TASK: Change the quantity of a cart line (+ or −). If it reaches 0, remove the line.
   HOW: Add d (+1 or −1) to cart[i].qty. For + we check the stock first. splice(i, 1) deletes the line when qty is 0 or less.
   IN THE SYSTEM: runs when the customer presses + or − inside My Order (acts.inc and acts.dec). */
function changeQty(i, d) {
  const l = cart[i];
  if (d > 0 && inCart(l.id) >= item(l.id).stock) return toast('No more stock for ' + item(l.id).name);
  l.qty += d; if (l.qty <= 0) cart.splice(i, 1);
  refresh();
}

/* TASK: Confirm the order: check the stock again, subtract it, save the order, and empty the cart.
   HOW: Stop with a message if the cart is empty or there is not enough stock. Then lower item.stock for each line, push a new order into S.orders
        (a text copy of the lines, the total, the name or table, status "Pending" and the time), then commit().
   IN THE SYSTEM: runs when the customer presses "Place order". The order then shows in Manage > Orders for the staff, and the stock numbers go down. */
function placeOrder() {
  if (!cart.length) return toast('Add something to your order first');
  for (const l of cart) if (inCart(l.id) > item(l.id).stock) return toast('Not enough stock for ' + item(l.id).name);
  const lines = cart.map(l => ({text: `${l.qty} × ${item(l.id).name}` + lineOpts(l).map(x => ' · ' + x).join('')}));
  cart.forEach(l => item(l.id).stock -= l.qty);
  const no = S.nextOrder++;
  S.orders.unshift({no, name: $('#cname').value.trim() || 'Walk-in', lines, total: cartTotal(), status: 'Pending', time: new Date().toLocaleString()});
  cart = []; $('#cname').value = ''; commit();
  document.body.classList.remove('drawer-open'); toast('Order #' + no + ' placed');
}

/* ---- 1.6 Buttons ----
   TASK: Make every button in the website work from ONE place.
   HOW: Each button in the HTML has data-act="name". When anything is clicked, we look for the closest element with data-act and run the function with that name from the list `acts`.
        The shared buttons are here. Each page adds its own with Object.assign(acts, {...}) in its section below.
   IN THE SYSTEM: this is why the HTML buttons have no onclick: they only have data-act. */
const acts = {
  drawer: () => document.body.classList.toggle('drawer-open'),
  inc: b => changeQty(+b.dataset.i, 1),
  dec: b => changeQty(+b.dataset.i, -1),
  place: placeOrder
};
document.addEventListener('click', e => { const b = e.target.closest('[data-act]'); if (b && acts[b.dataset.act]) acts[b.dataset.act](b); });


/* ==========================================================================
   2. HOME PAGE (index.html)
   The Home page only needs 3 numbers on the hero picture and the see-through top bar.
   ========================================================================== */

/* TASK: Fill the three numbers on the Home hero picture (drinks, meals, orders served).
   HOW: Count the items that are not "meals" (drinks), the items that are meals, and the orders with the status "Served".
   IN THE SYSTEM: only the Home page has #hstats, so on the other pages this function stops at the first line. */
function renderHero() {
  if (!$('#hstats')) return;
  const drinks = S.items.filter(i => i.cat !== 'meals').length, meals = S.items.length - drinks;
  const served = S.orders.filter(o => o.status === 'Served').length;
  $('#hstats').innerHTML = `<div><b>${drinks}</b>Drinks on the menu</div><div><b>${meals}</b>Meals on the menu</div><div><b>${served}</b>Orders served</div>`;
}

/* TASK: Make the top bar see-through over the hero picture, and solid brown after the user scrolls down.
   HOW: Add the class "solid" when scrollY is more than 40 (the CSS does the color). We run it once at the start and again on every scroll.
   IN THE SYSTEM: only for the Home page. The other pages already have the class "solid" in their HTML. */
function initHome() {
  const solidNav = () => $('#nav').classList.toggle('solid', scrollY > 40);
  addEventListener('scroll', solidNav, {passive: true}); solidNav();
}
function renderStatsH() {
  const sales = S.orders.reduce((s, o) => s + o.total, 0), pend = S.orders.filter(o => o.status === 'Pending').length;
  $('#stats2').innerHTML = `<div><b>${S.orders.length}</b>orders</div><div><b>${peso(sales)}</b>sales</div><div><b>${pend}</b>pending</div>`;
  $('#tc-orders2').textContent = pend || ''; $('#tc-msgs').textContent = S.msgs.length || '';
}

/* ==========================================================================
   3. MENU PAGE (menu.html)
   The customer part: choose a category or search, press +, pick size/add-ons, and the item goes to My Order.
   ========================================================================== */
let curCat = 'hot', pending = null, fullMenu = false;   // curCat = the chosen tab | pending = id of the item waiting in the size/add-ons dialog | fullMenu = "View Full Menu" is on

/* TASK: Draw the category tabs and the picture cards of the chosen category (or of all the items that match the search box).
   HOW: Build the HTML with map().join('') and put it in the page with innerHTML. 5 or less in stock shows a badge, 0 shows "Sold out" and disables the + button.
        If there is text in the search box (#q), we use matches() to show items from ALL categories as a grid.
   IN THE SYSTEM: this is the main part the customer sees. It runs at START, when a tab is clicked, when typing in the search box, and after the stock changes. */
function renderMenu() {
  if (!$('#items')) return;
  const q = $('#q').value.trim();   // the text typed in the search box
  const list = q ? S.items.filter(i => matches(i, q)) : S.items.filter(i => i.cat === curCat);
  $('#items').classList.toggle('grid', fullMenu || !!q);   // search results and "View Full Menu" are shown as a grid
  $('#tabs').innerHTML = Object.keys(CATS).map(c => `<button data-act="cat" data-v="${c}" class="${!q && c === curCat ? 'on' : ''}">${CATS[c].label}</button>`).join('');
  $('#items').innerHTML = list.map(i => {
    const out = i.stock <= 0, left = i.stock - inCart(i.id);
    const tag = out ? 'Sold out' : i.stock <= 5 ? i.stock + ' left' : '';
    return `<article class="card ${out ? 'out' : ''}">${picTag(i)}${tag ? `<span class="badge">${tag}</span>` : ''}
      <div class="glass"><small>${CATS[i.cat].label}</small><h4>${esc(i.name)}</h4><span>${i.p.map(peso).join(' / ')}</span>
      <button class="plus" data-act="add" data-id="${i.id}" aria-label="Add ${esc(i.name)}" ${left <= 0 ? 'disabled' : ''}>+</button></div></article>`;
  }).join('') || `<p class="note">${q ? 'No items match “' + esc(q) + '”.' : 'No items in this category yet. Add one in Manage.'}</p>`;
  const c = CATS[curCat];
  $('#catnote').textContent = q ? list.length + ' item(s) found. Click a category to go back.' : (c.sizes ? 'Prices shown as 8oz / 12oz. ' : '') + (c.add.length ? 'Add-ons: ' + c.add.map(a => `${a[0]} +${peso(a[1])}`).join(', ') + '.' : '');
}

/* TASK: Ask the customer for the size and add-ons before the item goes to My Order.
   HOW: Fill the <dialog id="dlg"> with radio buttons (sizes) and checkboxes (add-ons), then showModal() to open it.
   IN THE SYSTEM: runs when the customer presses the + on a card. The "Add to order" button closes the dialog, and the listener below continues the work. */
function openAdd(id) {
  const it = item(id), c = CATS[it.cat]; pending = id;
  $('#dt').textContent = it.name;
  $('#db').innerHTML = (c.sizes ? '<label>Size</label>' + c.sizes.map((s, i) => `<label><input type="radio" name="sz" value="${i}" ${i === 0 ? 'checked' : ''}>${s} (${peso(it.p[i])})</label>`).join('') : '')
    + (c.add.length ? '<label>Add-ons</label>' + c.add.map((a, i) => `<label><input type="checkbox" name="ad" value="${i}">${a[0]} +${peso(a[1])}</label>`).join('') : '<p>No size or add-ons for this item.</p>');
  $('#dlg').showModal();
}
// When the dialog is closed with "Add to order": read the chosen size and add-ons and send them to addToCart(). (This is how the pop-up talks to the cart.)
on('#dlg', 'close', () => {
  if ($('#dlg').returnValue !== 'ok' || pending == null) return;
  const sz = document.querySelector('input[name=sz]:checked');
  const add = [...document.querySelectorAll('input[name=ad]:checked')].map(x => +x.value);
  addToCart(pending, sz ? +sz.value : 0, add); pending = null;
});

/* TASK: Put the chosen item in My Order without going over the stock.
   HOW: Stop if the cart already has all the stock of that item. If the same item + size + add-ons is already in the cart, add 1 to qty, else push a new line.
   IN THE SYSTEM: called after the size/add-ons dialog. Then refresh() updates the cart, the number on the button and the cards. */
function addToCart(id, size, add) {
  if (inCart(id) >= item(id).stock) return toast('No more stock for ' + item(id).name);
  const key = JSON.stringify([id, size, add]);
  const found = cart.find(l => JSON.stringify([l.id, l.size, l.add]) === key);
  found ? found.qty++ : cart.push({id, size, add, qty: 1});
  refresh(); toast(item(id).name + ' added to My Order');
}

/* Menu page buttons (each name matches a data-act in menu.html):
   cat = the category tabs, add = the + button, full = "View Full Menu", prev / next = the arrows of the carousel */
Object.assign(acts, {
  cat: b => { curCat = b.dataset.v; $('#q').value = ''; renderMenu(); },   // choosing a category clears the search box
  add: b => openAdd(+b.dataset.id),
  full: b => { fullMenu = !fullMenu; b.textContent = fullMenu ? 'Show less' : 'View Full Menu'; renderMenu(); },
  prev: () => $('#items').scrollBy({left: -460, behavior: 'smooth'}),
  next: () => $('#items').scrollBy({left: 460, behavior: 'smooth'})
});

/* TASK: Search box of the Menu page: show the matching items while typing.
   HOW: The "input" event happens on every key press, so we just draw the menu again. renderMenu() reads what is in the box.
   IN THE SYSTEM: lets customers find a drink fast without clicking every category. */
on('#q', 'input', renderMenu);


/* ==========================================================================
   4. STORY PAGE (story.html): text only, nothing to program here
   ========================================================================== */


/* ==========================================================================
   5. CONTACT PAGE (contact.html)
   The message form. The messages are saved so the staff can read them in Manage.
   ========================================================================== */

/* TASK: Save the message from the Contact Us form so the staff can read it in Manage.
   HOW: preventDefault() stops the page from reloading. Then push {n: name, e: email, m: message} into S.msgs, save(), clear the form and show a toast.
   IN THE SYSTEM: the message appears in Manage > Messages (and the tab shows a number). */
on('#cform', 'submit', e => {
  e.preventDefault();
  S.msgs.unshift({n: $('#cn').value, e: $('#ce').value, m: $('#cm').value});
  save(); e.target.reset(); toast('Message sent. Thank you!');
});


/* ==========================================================================
   6. MANAGE PAGE (manage.html)
   The staff part, locked with a PIN: orders, menu + stock, and messages.
   ========================================================================== */

/* ---- 6.1 PIN gate ----
   TASK: Ask for a PIN before the Manage page opens.
   HOW: The PIN is written here in our program (MANAGE_PIN). Manage starts hidden and the PIN form (#gate) is shown. If the typed PIN is the same as MANAGE_PIN, Manage opens.
        sessionStorage remembers "unlocked" for this browser tab only, so leaving Manage (or pressing Lock) asks for the PIN again.
   IN THE SYSTEM: keeps the customers out of the staff page. To change the PIN, change MANAGE_PIN below.
   NOTE: anyone who opens script.js can read the PIN, so this is only simple protection for a school project (not real security). */
const MANAGE_PIN = '1234';   // <-- change this number to our own PIN
const UNLOCK = 'newlands-unlocked';
let fails = 0, lockUntil = 0;
// Remember (true) or forget (false) that this browser tab is unlocked. sessionStorage is cleared when the tab is closed.
function setUnlocked(yes) { try { yes ? sessionStorage.setItem(UNLOCK, '1') : sessionStorage.removeItem(UNLOCK); } catch (e) {} }
// Is this tab already unlocked? Used when Manage opens, so a page reload doesn't ask for the PIN again.
function isUnlocked() { try { return sessionStorage.getItem(UNLOCK) === '1'; } catch (e) { return false; } }

// TASK: Show the PIN form and hide the Manage content. Runs when Manage opens locked, and after pressing Lock.
function showGate() {
  $('#manage').hidden = true; $('#gate').hidden = false;
  $('#gpin').value = ''; $('#gerr').textContent = ''; $('#gpin').focus();
}
// TASK: Hide the PIN form, show the Manage content and draw it. Runs after the PIN is correct.
function openManage() { setUnlocked(true); $('#gate').hidden = true; $('#manage').hidden = false; renderManage(); }

/* TASK: Check the PIN that was typed.
   HOW: preventDefault() stops the form from reloading the page. Compare the typed PIN with MANAGE_PIN. 5 wrong tries in a row lock the form for 30 seconds (fails and lockUntil count that).
   IN THE SYSTEM: runs when the staff press "Unlock" in the PIN form. */
on('#gform', 'submit', e => {
  e.preventDefault();
  const err = t => $('#gerr').textContent = t;
  if (Date.now() < lockUntil) return err('Too many wrong tries. Wait ' + Math.ceil((lockUntil - Date.now()) / 1000) + ' seconds.');
  if ($('#gpin').value === MANAGE_PIN) { fails = 0; return openManage(); }
  $('#gpin').value = '';
  if (++fails >= 5) { fails = 0; lockUntil = Date.now() + 30000; return err('Too many wrong tries. Wait 30 seconds.'); }
  err('Wrong PIN. Try again.');
});

/* ---- 6.2 Top of the Manage page: the numbers and the tabs ---- */
/* TASK: Show the four numbers at the top (orders, sales, pending, low or sold out) and the small number badges on the tabs.
   HOW: Add up the totals of all orders for sales; count the pending orders, the items with 5 or less in stock, and the messages.
   IN THE SYSTEM: gives the staff a quick look at how the café is doing. */
function renderStats() {
  const sales = S.orders.reduce((s, o) => s + o.total, 0), pend = S.orders.filter(o => o.status === 'Pending').length;
  const low = S.items.filter(i => i.stock <= 5).length;
  $('#stats').innerHTML = `<div><b>${S.orders.length}</b>orders</div><div><b>${peso(sales)}</b>sales</div><div><b>${pend}</b>pending</div><div><b>${low}</b>low or sold out</div>`;
  $('#tc-orders').textContent = pend || ''; $('#tc-msgs').textContent = S.msgs.length || '';
}

/* TASK: Show one tab (Orders, Menu and Stocks, or Messages) and hide the other two.
   HOW: Give the class "on" to the clicked tab button, then set hidden = true to every .panel except the one with id "tab-<name>".
   IN THE SYSTEM: runs when the staff click a tab button in Manage (acts.tab). */
function showTab(t) {
  document.querySelectorAll('#mtabs button').forEach(b => b.classList.toggle('on', b.dataset.v === t));
  document.querySelectorAll('.panel').forEach(p => p.hidden = p.id !== 'tab-' + t);
}

/* TASK: Draw the whole Manage page.   HOW: It only calls the 4 small functions below, one for each part.
   IN THE SYSTEM: called by refresh() and right after the PIN is correct. */
function renderManage() {
  if (!$('#inv')) return;
  renderStats(); renderOrders(); renderInventory(); renderMessages();
}

/* ---- 6.3 Orders tab: what the customers ordered ---- */
/* TASK: List all the orders with a "Mark as served" button.
   HOW: Map S.orders to HTML. data-no tells the button which order to change. Served orders get the class "done" (the CSS makes them lighter).
   IN THE SYSTEM: the Orders tab. This is where the staff see what the customers ordered. */
function renderOrders() {
  $('#orders').innerHTML = S.orders.map(o => `<div class="order ${o.status === 'Served' ? 'done' : ''}">
    <div class="order-top"><b>#${o.no} · ${esc(o.name)}</b><b>${peso(o.total)}</b></div>
    <small>${esc(o.time)}</small>${o.lines.map(l => `<div>${esc(l.text)}</div>`).join('')}
    <p class="order-act"><button class="ghost" data-act="status" data-no="${o.no}">${o.status === 'Pending' ? 'Mark as served' : 'Served (undo)'}</button></p></div>`).join('') || '<p>No orders yet.</p>';
}

/* ---- 6.4 Menu and Stocks tab: the items, the stock, and the Add/Edit window ---- */
/* TASK: Show the items in a table (picture, name, category, price, stock, Edit, Remove). Only the items that match the search box (#mq) are shown.
   HOW: Filter S.items with matches(), then map them to table rows. The price and stock cells are <input>s with data-f, and the "change" listener below saves them.
   IN THE SYSTEM: the Menu and Stocks tab. This is how the staff control the stock and the menu. */
function renderInventory() {
  const rows = S.items.filter(i => matches(i, $('#mq').value));   // only the items that match the search box above the table
  $('#inv').innerHTML = rows.map(i => `<tr><td>${picTag(i, 'th')}
  </td>
  <td>${esc(i.name)}</td>
  <td>${CATS[i.cat].label}</td>
   <td>₱${i.p[0]}.00</td>
    <td>${i.stock}</td>
    <td><button class="ghost" data-act="edit" data-id="${i.id}">Edit</button> 
    <button class="ghost" data-act="del" data-id="${i.id}">Remove</button></td></tr>`).join('') || 
    '<tr><td colspan="6">No items match your search.</td></tr>';
}

/* TASK: Search box above the table: show only the matching items while typing.
   HOW: The "input" event happens on every key press, so we draw the table again. renderInventory() reads the box.
   IN THE SYSTEM: helps the staff find an item in a long menu. */
on('#mq', 'input', renderInventory);

/* "Add a menu item" / "Edit" window (one dialog for both). The functions below and the submit listener work together.
   TASK: Open the window, show a picture preview, and save a NEW item or the changes of an item.
   HOW: editId is null when adding and the item's id when editing. openModal() fills the form with the item's values when editing.
        "Picture file name" is optional: if empty, the item name is used. showPreview() tries the same file names as the menu does. We only save the file name, not the picture.
   IN THE SYSTEM: opened by "+ Add a menu item" (new item) and by the "Edit" button in the table (existing item). */
let editId = null;
// TASK: Show the small picture in the Add/Edit window. It tries the same file names as the menu, and shows the logo if the file is not found.
function showPreview() {
  const im = $('#pimg'), t = {name: $('#an').value, cat: $('#ac').value, img: $('#pf').value};
  im.classList.remove('def'); im.dataset.n = 0;
  if (!t.name.trim() && !t.img.trim()) { im.onerror = null; im.src = LOGO; return; }
  im._list = picList(t); im.onerror = () => nextPic(im); im.src = im._list[0];
}
// TASK: Update the price label and the folder hint when the category changes (hot drinks have an 8oz price, and each category has its own folder).
function catChanged() {
  const c = CATS[$('#ac').value];
  $('#aplab').textContent = c.sizes ? 'Price (₱) for 8oz (12oz ' + (editId == null ? 'is ₱20 more)' : 'keeps its gap)') : 'Price (₱)';
  $('#pathhint').textContent = `Put the picture file in images/${c.folder}/. Leave this empty to use the item name (e.g. latte.jpg).`;
}
// TASK: Open the Add/Edit window. With an item = Edit (the form is filled in), without = Add (empty form).
function openModal(title, button, it) {
  editId = it ? it.id : null; $('#addform').reset();
  $('#ntitle').textContent = title; $('#nsave').textContent = button;
  if (it) { $('#an').value = it.name; $('#ac').value = it.cat; $('#ap').value = it.p[0]; $('#as').value = it.stock; $('#pf').value = it.img || ''; }
  catChanged(); showPreview(); $('#ndlg').showModal();
}
// Update the labels and the preview while the staff change the category or type the name / file name.
on('#ac', 'change', () => { catChanged(); showPreview(); });
on('#an', 'input', showPreview);
on('#pf', 'input', showPreview);

/* TASK: Save the Add/Edit window: a NEW item, or the changes to the item being edited.
   HOW: If editing, copy the form values to the existing item (it keeps its 8oz/12oz price gap); if adding, push a new item with the next id. Then commit(), close the window and show a toast.
   IN THE SYSTEM: after saving, the menu cards, the table and the Home numbers all update. */
on('#addform', 'submit', e => {
  e.preventDefault();
  const c = $('#ac').value, price = +$('#ap').value, name = $('#an').value.trim(), stock = +$('#as').value, img = $('#pf').value.trim();
  const it = editId == null ? null : item(editId);
  if (it) {
    const gap = it.p.length > 1 ? it.p[1] - it.p[0] : 20;
    if (it.cat !== c) cart = cart.filter(l => l.id !== it.id);   // the old size/add-on numbers don't fit another category, so take this item out of My Order
    Object.assign(it, {name, cat: c, stock, img, p: CATS[c].sizes ? [price, price + gap] : [price]});
  } else S.items.push({id: S.nextId++, cat: c, name, p: CATS[c].sizes ? [price, price + 20] : [price], stock, img});
  commit(); $('#ndlg').close(); toast(it ? 'Item updated' : 'Menu item added');
});

/* ---- 6.5 Messages tab: what the customers sent in Contact Us ---- */
/* TASK: List the messages from the Contact Us page.   HOW: Map S.msgs to HTML.
   IN THE SYSTEM: the Messages tab. */
function renderMessages() {
  $('#msgs').innerHTML = S.msgs.map(m => `<div class="order"><b>${esc(m.n)}</b> (${esc(m.e)})<br>${esc(m.m)}</div>`).join('') || '<p>No messages yet.</p>';
}

/* Manage page buttons (the data-act names in manage.html):
   lock = lock again, tab = switch tab, status = served / pending, newitem and edit = open the Add/Edit window, closen = cancel it, del = remove an item, reset = delete all data */
Object.assign(acts, {
  tab: b => showTab(b.dataset.v),
  status: b => { const o = S.orders.find(o => o.no === +b.dataset.no); o.status = o.status === 'Pending' ? 'Served' : 'Pending'; commit(); },
  newitem: () => openModal('Add a menu item', 'Save item'),
  edit: b => openModal('Edit menu item', 'Save changes', item(+b.dataset.id)),
  closen: () => $('#ndlg').close(),
  del: b => { const it = item(+b.dataset.id); if (!confirm('Remove ' + it.name + ' from the menu?')) return; S.items = S.items.filter(i => i !== it); cart = cart.filter(l => l.id !== it.id); commit(); toast('Item removed'); },
});

/* TASK: Decide if the Manage page can open. 
   HOW: Fill the category list of the Add/Edit window first. If this tab is already unlocked, open Manage; if not, show the PIN form.
   IN THE SYSTEM: runs at START, but only on manage.html. */
function initManage() {
  $('#ac').innerHTML = Object.keys(CATS).map(c => `<option value="${c}">${CATS[c].label}</option>`).join('');
  if (isUnlocked()) openManage(); else showGate();
}


/* ==========================================================================
   7. START (runs once when any page opens)
   Steps: 
   1) add the shared parts, 
   2) load the saved cart, 
   3) draw the page, 
   4) run the setup of the page we are on.
   Leaving Manage forgets the unlock, so every visit to Manage asks for the PIN.
   This part is at the END of the file on purpose: the functions and data above must be ready first.
   ========================================================================== */
mountShell();
cart = read(CART_KEY, []).filter(l => item(l.id));
refresh();
if (page === 'home') initHome();
if (page === 'manage') initManage(); else setUnlocked(false);