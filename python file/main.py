"""
GENERAL NOTE AND REMINDERS

Newland - Coffee Shop Menu System (Console Edition -Python)

Features as the website: Home, Menu, Order, About us, Contact us,
and Menu Management (admin) with stock tracking.

Data is saved as JSON in the ./data folder, so it survives restarts.

All of us have assign Funtions to do,
Every function has a comment block with two parts:
    TASK = WHAT the function must do (the goal).
    HOW  = the steps you can follow to write or fix it.
Quick glossary used in the comments:
    function  = a named block of code you can run again and again.
    list      = an ordered group of things, e.g. [1, 2, 3].
    dict      = a group of label: value pairs, e.g. {"name": "Latte", "price": 120}.
    JSON file = a text file that stores lists and dicts so data is kept after
                the program closes.
    loop      = code that repeats (`while True` repeats until we `break`/`return`).
"""

import json
import os
from collections import Counter
from datetime import datetime


# Defaut Variables to use
SHOP_NAME = "Newland"
LOW_STOCK = 5
WIDTH = 62
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
MENU_FILE = os.path.join(DATA_DIR, "menu.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


DEFAULT_MENU = [
    {"id": 1, "name": "Espresso", "category": "Coffee", "price": 80.0, "stock": 20},
    {"id": 2, "name": "Americano", "category": "Coffee", "price": 95.0, "stock": 20},
    {"id": 3, "name": "Caffe Latte", "category": "Coffee", "price": 120.0, "stock": 20},
    {"id": 4, "name": "Caramel Macchiato", "category": "Coffee", "price": 140.0, "stock": 20},
    {"id": 5, "name": "Iced Matcha", "category": "Non-Coffee", "price": 130.0, "stock": 20},
    {"id": 6, "name": "Hot Chocolate", "category": "Non-Coffee", "price": 110.0, "stock": 20},
    {"id": 7, "name": "Butter Croissant", "category": "Pastry", "price": 75.0, "stock": 20},
    {"id": 8, "name": "Blueberry Muffin", "category": "Pastry", "price": 85.0, "stock": 20},
]


# ---------------------------------------------------------------- storage
#1 - DONE
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default
"""
    ASSIGN:____AHRON_____
    TASK:
        Read a JSON file and give back its data. If the file does not exist
        yet (first run) or is damaged, give back `default` instead of crashing.
    HOW:
        1. Open the file with `open(path, "r", encoding="utf-8")`.
        2. Turn its text into Python data with `json.load(f)` and return it.
        3. Put steps 1-2 inside `try:` and add
           `except (FileNotFoundError, json.JSONDecodeError):`
           so a missing or broken file does not stop the program.
        4. Inside that `except`, `return default`.
    """

#2 - DONE
def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)
"""
    ASSIGN:____AHRON_____
     TASK:
        Save Python data (list/dict) into a JSON file safely, so a crash in
        the middle of saving never leaves a half-written, broken file.
    HOW:
        1. Make sure the folder exists: `os.makedirs(folder, exist_ok=True)`.
        2. Write the data to a temporary file (path + ".tmp") using
           `json.dump(data, f, indent=2)` - indent=2 makes it readable.
        3. Swap the temp file in as the real file with `os.replace(tmp, path)`.
           (The swap happens in one step, so the real file is never half-done.)
    """

# ---------------------------------------------------------------- helpers
#3 DONE
def money(value):
    value = 1234.5
    price_text = f"PHP {value:,.2f}" 

"""
  ASSIGN:____KIM_____
    TASK:
        Turn a number like 1234.5 into a price text like "PHP 1,234.50".
    HOW:
        Use an f-string with a format code: f"PHP {value:,.2f}"
        (`,` adds thousands commas, `.2f` always shows 2 decimal places).
"""

#4
def line(char = "-" ):
    print(char * WIDTH)
"""
    ASSIGN:___JEN______
    TASK:
        Print a divider line so the screen looks organized.
    HOW:
        Multiply a character by the screen width: print(char * WIDTH).
        Example: "-" * 5 gives "-----".
    """

#5 pending
def title():
    print()
    print("=")
    print(text.center(WIDTH))
    print("=")    
"""
    ASSIGN:____KIM______
    TASK:
        Print a page title between two "=" lines, centered on the screen.
    HOW:
        1. print() an empty line for spacing.
        2. Call line("=") for the top border.
        3. print(text.center(WIDTH)) - `.center()` puts the text in the middle.
        4. Call line("=") again for the bottom border.
    """

#6
def pause():
    input("...")
"""
    ASSIGN:____JEN______
    TASK:
        Freeze the screen until the user presses Enter, so they have time
        to read what was printed before the next menu appears.
    HOW:
        Call input("...") and ignore what it returns. The program waits there.
    """

#7 DONE
def ask_text():
    while True:
        value = input(prompt).strip()

        if value or allow_blank:
            return value
        print("Please enter something")            
"""
    ASSIGN:_____KIM_____
    TASK:
        Ask the user to type text, and keep asking until they type something
        (unless blank is allowed). Returns the text without extra spaces.
    HOW:
        1. Start a `while True:` loop (repeats forever until we `return`).
        2. `value = input(prompt).strip()` - `.strip()` removes spaces at the
           start and end.
        3. If `value` has text (or allow_blank is True), `return value`.
        4. Otherwise print a friendly message; the loop asks again.
    """

#8 - DONE
def ask_number(prompt, kind=int, minimum=0, allow_blank=False):
    while True:
        raw = input(prompt).strip()

        if raw == "" and allow_blank:
            return None

        try:
            value = kind(raw)
        except ValueError:
            print("Invalid number, please try again.")
            continue

        if value < minimum:
            print(f"Number must be at least {minimum}.")
            continue

        return value
"""
    ASSIGN:____ROY______
    TASK:
        Ask for a number and keep asking until the user types a valid one that
        is not smaller than `minimum`. Use kind=int for whole numbers
        (quantity) and kind=float for decimals (price).
        If allow_blank is True and the user just presses Enter, return None.
    HOW:
        1. Loop with `while True:` and read `raw = input(prompt).strip()`.
        2. If raw is empty and allow_blank is True, `return None`.
        3. Try `value = kind(raw)` inside `try:`. If it fails with
           `except ValueError:`, print "invalid number" and `continue`
           (`continue` jumps back to the top of the loop).
        4. If `value < minimum`, print a message and `continue`.
        5. Otherwise `return value`.
    """

#9 DONE
def find_item(menu, item_id):
    for item in menu:
        if item["id"] == item_id:
           return item 

    return None
    
"""
    ASSIGN:____KIM______
    TASK:
        Look through the menu and give back the item whose "id" matches
        `item_id`. If there is no match, give back None.
    HOW:
        1. `for item in menu:` visits each item dict one by one.
        2. If `item["id"] == item_id`, `return item` right away.
        3. After the loop ends with no match, `return None`.
    """
#10 - DONE
def next_id():
    return max((i["id"] for i in menu), default=0) + 1
"""
    ASSIGN:_____ROY_____
    TASK:
        Make a new unique id for a new menu item (no two items share an id).
    HOW:
        Take the biggest existing id and add 1:
        `max((i["id"] for i in menu), default=0) + 1`.
        `default=0` handles an empty menu so the first item gets id 1.
    """
#11
def print_items():
    if not items:
        print("No items found." )
        return 
    print(f"{'ID':<4}{'Item':<24}{'Category':<12}{'Price':>10}{'Stock':>8} ")
    line(char = "-")
    for it in items: 
        print()
    
        
"""
    ASSIGN:_____JEN_____
    TASK:
        Show a list of menu items as a neat table with columns:
        ID, Item, Category, Price, Stock. Show "SOLD OUT" when stock is 0.
        If the list is empty, print "No items found."
    HOW:
        1. `if not items:` print the "No items found." message and `return`.
        2. Print a header row using f-string widths: `(f"{'ID':<4}{'Item':<24}{'Category':<12}{'Price':>10}{'Stock':>8}` means
           "left-align in 24 spaces", `{'Price':>10}` means "right-align in 10".
        3. Call line() for a divider.
        4. `for it in items:` build `stock` text ("SOLD OUT" if it["stock"] == 0,
           else str(it["stock"])) and print one row with the same widths.
"""

#12
# ---------------------------------------------------------------- pages
def home_page():
    title("WELCOME")
    print("Welcome to our shop! We're happy to see you.")
    print("Opening hours: Mon-Sat 7:00 AM - 7:00 PM, Sun 8:00 AM - 4:00 PM")

    picks = [i for i in menu if i["stock"] > 0][:3]

    print("\nToday's picks:")
    print_items(picks)
    pause()
"""
    ASSIGN:____ROY______
    TASK:
        Home page: greet the customer, show opening hours, and feature
        "Today's picks" - the first 3 items that are still in stock.
    HOW:
        1. Call title(...) with a welcome message.
        2. print() the welcome sentence and the opening hours.
        3. Build the picks with a list comprehension:
           `[i for i in menu if i["stock"] > 0][:3]`
           (keep items with stock above 0, then `[:3]` keeps only the first 3).
        4. Show them with print_items(), then call pause().
    """

#13 - DONE
def menu_page(menu):
    while True:
        title("OUR MENU")
        print("1. View all items\n2. Filter by category\n3. Search by name\n0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            print_items(menu)
        elif choice == "2":
            cats = sorted({i["category"] for i in menu})
            print("Categories:", ", ".join(cats))
            cat = ask_text("Category: ").lower()
            print_items([i for i in menu if i["category"].lower() == cat])
        elif choice == "3":
            term = ask_text("Search: ").lower()
            print_items([i for i in menu if term in i["name"].lower()])
        elif choice == "0":
            return
        else:
            print("  Invalid choice.")
            continue
        pause()
"""
    ASSIGN:_____AHRON_____
     TASK:
        Customer menu page with a small sub-menu: view all items, filter by
        category, or search by name. Option 0 goes back to the main menu.
    HOW:
        1. Use `while True:` so the sub-menu keeps showing until the user picks 0.
        2. print the options and read `choice = input("Choose: ").strip()`.
        3. Use `if / elif / else` on `choice`:
           "1" -> print_items(menu)
           "2" -> collect categories with a set `{i["category"] for i in menu}`,
                  ask for one, then show items where the category matches
                  (compare with `.lower()` so "coffee" equals "Coffee").
           "3" -> ask for a word; show items where the word is `in` the
                  item's name (also compared in lowercase).
           "0" -> `return` (this ends the function and goes back).
           anything else -> print "Invalid choice." and `continue`.
        4. After showing results, call pause().
    """

#14
def about_page():
    title("ABOUT US")
    print("About Newlands")
    print("Newlands started with one espresso machine and a short menu. We still keep it short: a handful of coffees, a few cold drinks, and pastries that arrive each morning.")
    print("")
"""
    ASSIGN:_____ROY_____
    TASK:
        About us page: tell the story of the shop.
    HOW:
        1. Call title("ABOUT US").
        2. Use several print() lines with your own shop story (replace the
           sample text).
        3. End with pause(). No data or loops are needed here.
    """

#15
def contact_page():
    title("CONTACT US")
    print("Sisters of Mary - Adlas, Campus, Brgy. Adlas, Silang, 4118 Cavite")
    print("(000) 123-4567")
    print("hello@newlandsexample")
    print("Mon to Sat 7am to 7pm, Sun 8am to 4pm")

"""
    ASSIGN:____JEN______
    TASK:
        Contact us page: show address, phone, email, and opening hours.
    HOW:
        1. Call title("CONTACT US").
        2. print() one line per detail (replace the sample details with real ones).
        3. End with pause().
    """
#16
# ---------------------------------------------------------------- ordering
#def cart_total():
"""
    ASSIGN:____ROY______
    TASK:
        Compute the total price of everything in the cart.
        The cart is a dict: {item_id: quantity}, e.g. {1: 2, 7: 1}.
    HOW:
        For every pair `item_id, qty` in `cart.items()`, look up the item with
        find_item(), multiply its price by qty, and add them all with `sum(...)`.
    """

#17
#def show_cart():
"""
    ASSIGN:_____ROY_____
    TASK:
        Print what the customer has ordered so far, with a line total for each
        item and a grand total at the bottom. Show "(empty)" if nothing yet.
    HOW:
        1. print the "YOUR CART" heading and a divider.
        2. `if not cart:` print "(empty)" and `return`.
        3. `for item_id, qty in cart.items():` find the item with find_item()
           and print "qty x name   price*qty".
        4. Print a divider and the grand total using cart_total().
    """

#18 - DONE
def print_receipt(receipt):
    title(f"{SHOP_NAME.upper()} - RECEIPT")
    print(f"Order #{order['order_no']:04d}    {order['date']}")
    print(f"Customer: {order['customer']}")
    line()
    for it in order["items"]:
        print(f"  {it['qty']} x {it['name']:<22}{it['price'] * it['qty']:>10.2f}")
    line()
    print(f"  {'Total':<26}{order['total']:>10.2f}")
    print(f"  {'Paid':<26}{order['paid']:>10.2f}")
    print(f"  {'Change':<26}{order['change']:>10.2f}")
    print("\nThank you! Come again.")

"""
    ASSIGN:_____AHRON_____
    TASK:
        Print the final receipt for a finished order: order number, date,
        customer, each item, then total, amount paid, and change.
    HOW:
        1. title(...) with the shop name, then print the order number
           (`{order['order_no']:04d}` pads it like 0007) and date.
        2. print the customer name and a divider.
        3. Loop over `order["items"]` and print one row per item.
        4. Print total, paid, and change using the same column widths,
           and finish with a thank-you message.
    """

#19
#def checkout():
"""
    ASSIGN:____ROY______
    TASK:
        Finish an order: take the payment, subtract the sold quantities from
        stock, save the order history, and print the receipt.
        Returns True if the order was completed, False if the cart was empty.
    HOW:
        1. If the cart is empty, print a message and `return False`.
        2. Get the total with cart_total(), then ask the customer's name.
        3. Ask for the amount paid with ask_number(..., float, 0) inside a
           `while True:` loop; only `break` when paid >= total.
        4. For each item in the cart, subtract qty from `item["stock"]` and
           collect {"name", "qty", "price"} into a list called `items`.
        5. save_json(MENU_FILE, menu) so the new stock levels are kept.
        6. Load the old orders with load_json(ORDERS_FILE, []), build one new
           order dict (order_no = number of old orders + 1, date from
           `datetime.now().strftime(...)`, change = paid - total),
           append it, and save_json(ORDERS_FILE, orders).
        7. print_receipt(order) and `return True`.
    """

#20
#def order_page():
"""
    ASSIGN:____ROY______
    TASK:
        The ordering system. The customer builds a cart (add / remove items),
        then checks out. The cart must never hold more of an item than we
        have in stock.
    HOW:
        1. Create an empty dict `cart = {}` (item_id -> quantity).
        2. Loop with `while True:` and each time show the items in stock
           (print_items) and the cart (show_cart), then the options:
           1 Add, 2 Remove, 3 Checkout, 0 Cancel.
        3. Option 1 (Add): ask for the item id, use find_item(); if it is None
           or its stock is 0, print a message and `continue`. Ask for the
           quantity. Check `already_in_cart + qty > item["stock"]` - if true,
           tell the user how many are left and `continue`. Otherwise update
           the cart: `cart[id] = cart.get(id, 0) + qty`.
        4. Option 2 (Remove): `cart.pop(item_id, None)` deletes the item from
           the cart; it gives back None when the item was not in the cart.
        5. Option 3 (Checkout): call checkout(menu, cart); if it returns True,
           call pause() and `return`.
        6. Option 0: `return` (cancel the order).
    """


# ---------------------------------------------------------------- admin
#21 - DONE
def add_item(menu):
    name = ask_text("Name: ")
    if any(i["name"].lower() == name.lower() for i in menu):
        print("  That item already exists.")
        return
    category = ask_text("Category (Coffee/Non-Coffee/Pastry/...): ")
    price = ask_number("Price: PHP ", float, 0.01)
    stock = ask_number("Starting stock: ", int, 0)
    menu.append({"id": next_id(menu), "name": name, "category": category,
                 "price": price, "stock": stock})
    save_json(MENU_FILE, menu)
    print("  Item added.")
"""
    ASSIGN:____AHRON______
     TASK:
        Add a brand-new item to the menu with a starting stock.
        Two items must not have the same name.
    HOW:
        1. Ask for name (ask_text), category (ask_text), price
           (ask_number(..., float, 0.01)) and starting stock (ask_number(..., int, 0)).
        2. Duplicate check: `any(i["name"].lower() == name.lower() for i in menu)`
           is True if the name already exists - if so, print a message and `return`.
        3. Build a new dict with id=next_id(menu) and `menu.append(new_item)`.
        4. save_json(MENU_FILE, menu) and print "Item added."
    """

#22 - DONE
def edit_item(menu):
    item = find_item(menu, ask_number("Item ID to edit: ", int, 1))
    if not item:
        print("  Item not found.")
        return
    print("Leave blank to keep the current value.")
    item["name"] = ask_text(f"Name [{item['name']}]: ", True) or item["name"]
    item["category"] = ask_text(f"Category [{item['category']}]: ", True) or item["category"]
    price = ask_number(f"Price [{item['price']}]: PHP ", float, 0.01, True)
    if price is not None:
        item["price"] = price
    save_json(MENU_FILE, menu)
    print("  Item updated.")
"""
    ASSIGN:___AHRON_______
    TASK:
        Change an existing item's name, category, or price. Pressing Enter
        on a question keeps the old value.
    HOW:
        1. Ask for the item id and find it with find_item(); if None, print
           "Item not found." and `return`.
        2. For name and category use ask_text(..., True) (blank allowed) and
           the trick `new_value or old_value` - an empty string counts as
           False, so the old value is kept.
        3. For price use ask_number(..., float, 0.01, True); it returns None
           when blank, so only change the price `if price is not None`.
        4. save_json(MENU_FILE, menu) and print "Item updated."
    """

#23 - DONE
def restock_item(menu):
    item = find_item(menu, ask_number("Item ID to restock: ", int, 1))
    if not item:
        print("  Item not found.")
        return
    qty = ask_number(f"Add how many to {item['name']} (now {item['stock']})? ", int, 1)
    item["stock"] += qty
    save_json(MENU_FILE, menu)
    print(f"  {item['name']} stock is now {item['stock']}.")
"""
    ASSIGN:_____AHRON_____
    TASK:
        Stock tracking: add newly delivered stock to an item
        (e.g. 20 more croissants arrived).
    HOW:
        1. Ask for the item id, find_item(); if None, print a message and `return`.
        2. Ask how many to add with ask_number(..., int, 1) (at least 1).
        3. Add it: `item["stock"] += qty` (same as stock = stock + qty).
        4. save_json(MENU_FILE, menu) and print the new stock level.
    """


#24
#def delete_item():
"""
    ASSIGN:_____ROY_____
    TASK:
        Remove an item from the menu, but only after the admin confirms,
        so nothing is deleted by accident.
    HOW:
        1. Ask for the item id, find_item(); if None, print a message and `return`.
        2. Ask "Delete <name>? (y/n)" and compare the answer, in lowercase,
           with "y".
        3. If yes: `menu.remove(item)`, then save_json(MENU_FILE, menu) and
           print "Item deleted." If no, do nothing.
    """

#25
#def low_stock_report():
"""
    ASSIGN:____ROY______
    TASK:
        Show items that are sold out or running low, so the admin knows
        what to restock. "Low" means LOW_STOCK (5) or fewer.
    HOW:
        Build a filtered list with a list comprehension
        `[i for i in menu if i["stock"] <= LOW_STOCK]` and show it with
        print_items().
    """
#26
#def sales_report():
"""
    ASSIGN:__Roy____
    TASK:
        Summarize sales: number of orders, total revenue, and the top 3
        best-selling items.
    HOW:
        1. orders = load_json(ORDERS_FILE, []); if it is empty, print
           "No orders yet." and `return`.
        2. Create `sold = Counter()`. A Counter is a dict that counts things.
        3. Loop over every order and every item in it, and add the quantity:
           `sold[it["name"]] += it["qty"]`.
        4. Revenue = `sum(o["total"] for o in orders)`.
        5. `sold.most_common(3)` gives the 3 biggest sellers as (name, qty) pairs.
    """

#27 - DONE
def admin_page(menu):
    for _ in range(3):
        if input("Admin PIN: ").strip() == ADMIN_PIN:
            break
        print("  Wrong PIN.")
    else:
        print("  Too many attempts.")
        return
    actions = {
        "2": lambda: add_item(menu),
        "3": lambda: edit_item(menu),
        "4": lambda: restock_item(menu),
        "5": lambda: delete_item(menu),
        "6": lambda: low_stock_report(menu),
        "7": sales_report,
    }
    while True:
        title("MENU MANAGEMENT")
        print("1. View all items   2. Add item      3. Edit item")
        print("4. Restock item     5. Delete item   6. Low stock report")
        print("7. Sales report     0. Back")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        if choice == "1":
            print_items(menu)
        elif choice in actions:
            actions[choice]()
        else:
            print("  Invalid choice.")
            continue
        pause()

"""
    ASSIGN:__AHRON_____
    TASK:
        The menu-management console. It is protected by a PIN, and lets the
        admin view, add, edit, restock, and delete items, and see reports.
    HOW:
        1. PIN check: `for _ in range(3):` gives 3 tries. If the typed PIN
           equals ADMIN_PIN, `break`. The `else:` attached to the `for` runs
           only when the loop finished without a break - print "Too many
           attempts." and `return`.
        2. Make a dict `actions` that maps each choice ("2", "3", ...) to the
           function to run. `lambda: add_item(menu)` wraps a function call
           so it runs later, only when chosen.
        3. Loop with `while True:`, print the options, read the choice.
        4. "0" -> `return`; "1" -> print_items(menu); a choice found in
           `actions` -> call it with `actions[choice]()`; else print
           "Invalid choice." and `continue`.
        5. Call pause() after each action.
    """

# ---------------------------------------------------------------- main
#28 - DONE
def main():
    menu = load_json(MENU_FILE, None)
    if menu is None:
        menu = DEFAULT_MENU
        save_json(MENU_FILE, menu)
    while True:
        title(SHOP_NAME.upper())
        print("1. Home\n2. Menu\n3. Order\n4. About us\n5. Contact us")
        print("6. Menu management (admin)\n0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            home_page(menu)
        elif choice == "2":
            menu_page(menu)
        elif choice == "3":
            order_page(menu)
        elif choice == "4":
            about_page()
        elif choice == "5":
            contact_page()
        elif choice == "6":
            admin_page(menu)
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("  Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

"""
    ASSIGN:__AHRON_____
    TASK:
        Start the program: load the menu (or create the default one on the
        very first run) and keep showing the main menu until the user exits.
    HOW:
        1. `menu = load_json(MENU_FILE, None)`. If it is None (no file yet),
           use DEFAULT_MENU and save it with save_json().
        2. Loop with `while True:`, print the 7 options, read the choice.
        3. Send each choice to its page function (home_page, menu_page,
           order_page, about_page, contact_page, admin_page).
        4. "0" prints "Goodbye!" and `return`, which ends the program.
        5. Always pass the SAME `menu` list to the pages - they change it in
           place, so every page sees the latest stock.
"""
