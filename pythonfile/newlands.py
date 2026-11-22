"""
Newland's Coffee - Menu and Ordering System (Console Edition)

Hi team! This is the terminal (console) version of our coffee shop system.
The menu, prices and About text come from the Newland's menu PDF.
It has the same parts as our website idea: Home, Menu, Order (sizes + add-ons),
About us, Contact us, and Menu Management (admin) with stock tracking.

Run:   python newlands.py --(MAKE THE FILE DIRECTORY CORRECT)--.
Admin PIN: 1234  for default PIN
Our data is saved as JSON files in the ./data folder.

HOW TO READ THIS FILE (it's our first big project, so I wrote the comments as
simple as I could!)
Every function has 3 notes:
    TASK          = what the function is supposed to do
    HOW           = the steps we can follow to code it (or fix it if it breaks)
    IN THE SYSTEM = where it is used in the program, so we know which part of
                    the shop it affects
Words we keep seeing:
    function  = a named block of code that we can run again and again.
    list      = a group of things in order, like [1, 2, 3].
    dict      = a group of label: value pairs, like {"name": "Latte", "price": 80}.
    JSON file = a text file that keeps our lists and dicts after the program closes.
    loop      = code that repeats. `while True` repeats until we `break` or `return`.
Our menu is a LIST of DICTS. Each dict is one item, for example:
    {"id": 38, "name": "Latte", "category": "Hot", "price": 80.0,
     "sizes": {"8oz": 80.0, "12oz": 100.0}, "note": "", "stock": 20}

BIG PICTURE (how the whole program flows)
    main() loads the menu and shows the main menu. Each choice opens a page:
      Home / Menu / About / Contact -> only SHOW information.
      Order -> the customer builds a cart, then checkout() saves the order
               and lowers the stock.
      Admin -> (PIN first) add / edit / restock / delete items, see reports.
    Every page shares the same `menu` list, so when stock changes in one
    place, all the other pages see the new number right away.
"""
import json
import os
import textwrap
from collections import Counter
from datetime import datetime

SHOP_NAME = "Newland's"
ADMIN_PIN = "1234"
LOW_STOCK = 5          # "low stock"
DEFAULT_STOCK = 20     # default stock for new items
WIDTH = 62
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
MENU_FILE = os.path.join(DATA_DIR, "newlands_menu.json")
ORDERS_FILE = os.path.join(DATA_DIR, "newlands_orders.json")

# Contact info for the Contact page.
CONTACT_ADDRESS = "Sisters of Mary School - Adlas, Inc. Brgy. Adlas, Silang, Cavite"
CONTACT_PHONE = "+6391-2345-67890"

# Order of the sections.
CATEGORIES = ["Meal", "Iced", "Frappe", "Fizz", "Hot", "Brewed"]

# These is only for Hot drinks come in two sizes.
SIZES = ["8oz", "12oz"]

# Add-ons for each category: {category: {add-on name: price}}.

ADDONS = {
    "Meal": {"Extra Rice": 25, "Extra Egg": 20},
    "Iced": {"Espresso": 40, "Upsize": 25},
    "Frappe": {"Upsize": 25},
    "Fizz": {"Upsize": 10, "Sinkers": 20},
    "Hot": {"Espresso": 40},
    "Brewed": {},
}

# The Menu data: {category: [(name, price), description(optional)]}.
# Hot drinks use a price pair (8oz, 12oz). Brewed items have a 3rd value:
# a short description.
MENU_DATA = {
    "Meal": [
        ("Soy Garlic Chicken", 159), ("Breaded Porkchop", 179),
        ("Boneless Bangus", 169), ("Tocilog", 149), ("Hotsilog", 139),
        ("Longsilog", 149), ("Corned Beef Silog", 149),
        ("Fried Pork Belly", 179), ("Fried Pork Chop", 179),
    ],
    "Iced": [
        ("Iced Americano", 80), ("Iced Spanish Latte", 125),
        ("Iced Caramel Macchiato", 125), ("Iced Cappuccino", 125),
        ("Iced Vanilla Latte", 125), ("Iced Hazelnut Latte", 125),
        ("Iced Mocha Latte", 125), ("Iced Salted Caramel Latte", 125),
        ("Iced Strawberry Matcha", 150), ("Iced Matcha Latte", 125),
        ("Iced Chocolate Latte", 125),
    ],
    "Frappe": [(n, 150) for n in (
        "Strawberry Frappe", "Blueberry Frappe", "Matcha Frappe",
        "Mocha Frappe", "Caramel / Salted Frappe", "Coffee Jelly Frappe",
        "Java Chip Frappe", "Cookies and Cream Frappe", "Green Apple Frappe")],
    "Fizz": [(n, 120) for n in (
        "Strawberry Fizz", "Blueberry Fizz", "Green Apple Fizz", "Mango Fizz",
        "Blue Curacao Fizz", "Lemon Fizz", "Passion Fruit Fizz",
        "Sparkling Americano Fizz")],
    "Hot": [
        ("Latte", (80, 100)), ("Americano", (60, 80)),
        ("Matcha Latte", (100, 120)), ("Cappuccino", (80, 100)),
        ("Spanish Latte", (100, 120)), ("Chocolate Latte", (100, 120)),
        ("Caramel Macchiato", (100, 120)), ("Vanilla Latte", (100, 120)),
        ("Herbal Tea", (50, 70)),
    ],
    "Brewed": [
        ("French Press", 120, "A rich, full-bodied coffee with deep aromas "
                              "and a velvety mouthfeel."),
        ("Chemex Pour Over", 150, "A clean, well-balanced cup with delicate "
                                  "flavor notes and a refreshing aroma."),
        ("Siphon Brewer", 200, "An aromatic, refined cup with a silky texture "
                               "and complex layers of flavor."),
        ("V60 Dripper", 150, "A pour-over that highlights the coffee's "
                             "natural sweetness, acidity, and origin."),
    ],
}

# Detail of the "About" page.
ABOUT_PARAGRAPHS = [
    "Newland's was inaugurated on March 16 through the generosity of the "
    "benefactors of the Sisters of Mary. It is a school-based coffee shop and "
    "a TESDA-registered Barista NC II Assessment Center, giving students a "
    "place to practice their skills and experience working in an actual "
    "coffee shop.",
    "Our baristas are students of the Sisters of Mary School, guided and "
    "supervised by their instructors. Every cup they prepare and serve is an "
    "opportunity to improve their skills, build confidence, and prepare for "
    "future employment in the coffee industry.",
    "Newland's operates on a non-profit basis, and every purchase helps "
    "support the mission of the Sisters of Mary in providing education and "
    "vocational training to young people from poor families. When you visit "
    "Newland's Cafe, you are not just buying coffee - you are helping our "
    "students build a better future.",
    "Come, enjoy your favorite drink, support our student baristas, and be "
    "part of their journey, one cup at a time!",
    "At Newland's, every cup helps a student learn, every order builds "
    "experience, and every customer becomes part of our mission.",
]


# ================================================================ STORAGE

"""
    Assign:__AHRON__
    TASK:
        This one reads a JSON file and gives us the data inside. If the file isn't
        there yet (like the very first time we run the program) or it got messed
        up, we don't want a crash, so it just gives back `default` instead.
    HOW:
        1. Open the file with `open(path, "r", encoding="utf-8")`.
        2. `json.load(f)` turns the text in the file into Python data (lists and
           dicts) and we return it.
        3. Put steps 1 and 2 inside `try:` and catch FileNotFoundError and
           json.JSONDecodeError with `except`. This is how we stop an error from
           crashing the whole program.
        4. Inside the `except`, just `return default`.
    IN THE SYSTEM:
        main() uses it to load the menu when the program starts. checkout() and
        sales_report() use it to load the saved orders.
"""
def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


    """
    ASSING: __AHRON__
    TASK:
        Saves our data (the menu or the orders) into a JSON file. We want it safe,
        so if the program crashes while saving, the real file doesn't end up
        half-written and broken.
    HOW:
        1. `os.makedirs(folder, exist_ok=True)` makes the data folder if it isn't
           there yet.
        2. Write everything into a temporary file (path + ".tmp") with
           `json.dump(data, f, indent=2)`. indent=2 just makes the file easy for
           us to read.
        3. `os.replace(tmp, path)` swaps the temp file in as the real file in one
           step.
    IN THE SYSTEM:
        Called every time something changes (new order, stock deducted, item
        added / edited / restocked / deleted, menu reset) so the changes are still
        there the next time we open the program.
    """
def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


# ================================================================ HELPERS

    """
    ASSIGN: __KIM__
    TASK:
        Turns a number like 1234.5 into price text like "PHP 1,234.50" so all our
        prices look the same everywhere.
    HOW:
        Use an f-string with a format code: f"PHP {value:,.2f}". The `,` adds the
        thousands commas and `.2f` means always show 2 decimal places.
    IN THE SYSTEM:
        Used for the "Total due" at checkout and the total revenue in the sales
        report.
    """
def money(value):
    return f"PHP {value:,.2f}"



    """
    ASSIGN: __JEN__
    TASK:
        Prints a divider line so the screen looks neat and organized.
    HOW:
        Multiply a character by the screen width: `char * WIDTH`.
        (Example: "-" * 5 gives "-----".)
    IN THE SYSTEM:
        Used under the table headers, in the cart and the receipt, and by title()
        for the "=====" borders.
    """
def line(char="-"):
    print(char * WIDTH)



    """
    ASSIGN: __KIM__
    TASK:
        Prints a page title in the middle of two "=" lines. Every screen starts
        with this, so it feels like we changed pages.
    HOW:
        1. print() an empty line for spacing.
        2. line("=") for the top border.
        3. print(text.center(WIDTH)) - `.center()` puts the text in the middle.
        4. line("=") again for the bottom border.
    IN THE SYSTEM:
        Top of the main menu, Menu page, Order page, About, Contact, Admin page and
        the receipt.
    """
def title(text):
    print()
    line("=")
    print(f"{text.center(WIDTH)}")
    line("=")


    """
    ASSIGN: __JEN__
    TASK:
        Waits until the user presses Enter so they can read the screen first
        (without it, the next menu shows up right away and the text scrolls away).
    HOW:
        Call `input("...")` and just ignore whatever it returns. The program waits
        there until Enter is pressed.
    IN THE SYSTEM:
        Used at the end of the Home, About and Contact pages, after menu results,
        after each admin action, and after the receipt.
    """
def pause():
    input("\nPress Enter to continue...")



    """
    ASSIGN: __KIM__
    TASK:
        Asks the user to type some text and keeps asking until they really type
        something (unless blank is allowed). Gives back the text without extra
        spaces.
    HOW:
        1. Start a `while True:` loop (it repeats until we `return`).
        2. `value = input(prompt).strip()` - `.strip()` removes the spaces at the
           start and the end.
        3. If `value` has text (or allow_blank is True), `return value`.
        4. Otherwise print a friendly message and the loop asks again.
    IN THE SYSTEM:
        Used for the customer name at checkout, the search word on the Menu page,
        and the names / descriptions in the admin page.
    """
def ask_text(prompt, allow_blank=False):
    while True:
        value = input(prompt).strip()
        if value or allow_blank:
            return value
        print("  Please enter something.")


    """
    ASSIGN: __ROY__
    TASK:
        Asks for a number and keeps asking until the user types a valid one that
        is not smaller than `minimum`. Use kind=int for whole numbers (quantity)
        and kind=float for decimals (price). If allow_blank is True and the user
        just presses Enter, it gives back None.
    HOW:
        1. `while True:` loop, then `raw = input(prompt).strip()`.
        2. If raw is empty and allow_blank is True, `return None`.
        3. `try: value = kind(raw)`. If it fails, `except ValueError:` prints
           "invalid number" and `continue` (jumps back to the top of the loop).
        4. If `value < minimum`, print a message and `continue`.
        5. Otherwise `return value`.
    IN THE SYSTEM:
        Used almost everywhere we need a number: item IDs, quantity, amount paid,
        prices and stock. One function for all of them means the program doesn't
        crash when someone types letters.
    """
def ask_number(prompt, kind=int, minimum=0, allow_blank=False):
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_blank:
            return None
        try:
            value = kind(raw)
        except ValueError:
            print("  Please enter a valid number.")
            continue
        if value < minimum:
            print(f"  Value must be at least {minimum}.")
            continue
        return value



    """
    ASSIGN: __KIM__
    TASK:
        Looks through the menu for the item that has a certain id. Gives back the
        item (a dict), or None if there's no match.
    HOW:
        1. `for item in menu:` checks the items one by one.
        2. If `item["id"] == item_id`, `return item` right away.
        3. If the loop ends with no match, `return None`.
    IN THE SYSTEM:
        Turns an id that the user typed into the real item. Ordering uses it (add
        to cart, cart total, checkout) and so do the admin edit / restock / delete.
    """
def find_item(menu, item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None



    """
    ASSIGN: __ROY__
    TASK:
        Makes a new unique id for a new menu item so no two items share an id.
    HOW:
        Take the biggest id we have and add 1:
        `max((i["id"] for i in menu), default=0) + 1`.
        The `default=0` is for an empty menu, so the first item gets id 1.
    IN THE SYSTEM:
        Only used by add_item() in the admin page.
    """
def next_id(menu):
    return max((i["id"] for i in menu), default=0) + 1


# ================================================================ MENU DATA

    """
    ASSIGN: __AHRON__
    TASK:
        Turns the MENU_DATA table (the PDF menu) into our real menu: a list of item
        dicts, each with id, name, category, price, sizes, note and stock.
    HOW:
        1. Start with an empty list `menu = []`.
        2. Loop over CATEGORIES (so the order matches the printed menu), then over
           every entry in MENU_DATA[category].
        3. `for name, price, *rest in ...` - the `*rest` collects any extra values
           (the Brewed description). `rest[0] if rest else ""` reads it safely.
           (I had to look this star thing up!)
        4. If `price` is a tuple (the Hot drinks), pair each size with its price
           using `zip(SIZES, price)` inside a dict. The plain `price` field then
           holds the 8oz price.
        5. The id is `len(menu) + 1`, so ids go 1, 2, 3... in order.
    IN THE SYSTEM:
        main() calls it the first time the program runs (no saved menu yet), and
        reset_menu() calls it to bring back the original menu.
    """
def build_default_menu():
    menu = []
    for category in CATEGORIES:
        for name, price, *rest in MENU_DATA[category]:
            item = {"id": len(menu) + 1, "name": name, "category": category,
                    "price": 0.0, "sizes": {},
                    "note": rest[0] if rest else "", "stock": DEFAULT_STOCK}
            if isinstance(price, tuple):
                item["sizes"] = {s: float(p) for s, p in zip(SIZES, price)}
                item["price"] = float(price[0])
            else:
                item["price"] = float(price)
            menu.append(item)
    return menu


# ================================================================ DISPLAY
def price_text(item):
    """
    TASK:
        Gives the price of an item as short text. Normal items show "150". Hot
        drinks with two sizes show "80 / 100" (8oz / 12oz).
    HOW:
        1. If `item["sizes"]` is not empty, join all the size prices with " / ".
        2. Otherwise format the single price.
        3. The `:g` format code removes useless zeros, so 80.0 shows as 80.
    IN THE SYSTEM:
        Used by print_items() to fill the Price column of every menu table.
    """
    if item["sizes"]:
        return " / ".join(f"{p:g}" for p in item["sizes"].values())
    return f"{item['price']:g}"



    """
    ASSIGN: __AHRON__
    TASK:
        Shows a list of items as a neat table: ID, Item, Category, Price, Stock.
        Shows "SOLD OUT" when the stock is 0, prints the description under the row
        if the item has one (Brewed items), and prints "No items found." if the
        list is empty.
    HOW:
        1. `if not items:` print the message and `return`.
        2. Print a header row using f-string widths: `{'Item':<26}` means
           "left-align in 26 spaces" and `{'Price':>11}` means "right-align in 11".
        3. Call line() for a divider.
        4. `for it in items:` build the stock text, then print one row using
           price_text(it). If `it.get("note")` has text, print it with
           `textwrap.fill(...)`, which wraps long text to fit the screen.
    IN THE SYSTEM:
        This is our main "show items" function. The Menu page, the Order page,
        search results, the Home featured list, the admin views and the low stock
        report all use it.
    """
def print_items(items):
    if not items:
        print("  No items found.")
        return
    print(f"{'ID':<4}{'Item':<26}{'Category':<9}{'Price':>11}{'Stock':>8}")
    line()
    for it in items:
        stock = "SOLD OUT" if it["stock"] == 0 else str(it["stock"])
        print(f"{it['id']:<4}{it['name'][:24]:<26}{it['category'][:8]:<9}"
              f"{price_text(it):>11}{stock:>8}")
        if it.get("note"):
            print(textwrap.fill(it["note"], WIDTH - 4,
                                initial_indent="    ", subsequent_indent="    "))


    """
    ASSIGN: __AHRON__
    TASK:
        Prints the add-ons of one category, like the bottom of each page of the
        printed menu: "Add-ons: Extra Rice +25, Extra Egg +20". For Hot drinks it
        also explains that the price shows 8oz / 12oz.
    HOW:
        1. `ADDONS.get(category, {})` gets the add-ons (an empty dict if there are
           none).
        2. If there are any, print them joined with ", " using an f-string like
           f"{name} +{price}".
        3. `if category == "Hot":` print the sizes note.
    IN THE SYSTEM:
        Called by print_grouped_menu() and by "Browse a category" in menu_page(),
        so customers can see the add-on prices before they order.
    """
def print_addons(category):
    addons = ADDONS.get(category, {})
    if addons:
        print("  Add-ons: " + ", ".join(f"{n} +{p}" for n, p in addons.items()))
    if category == "Hot":
        print(f"  Sizes: price is shown as {' / '.join(SIZES)}")


    """
    ASSIGN: __AHRON__
    TASK:
        Prints the whole menu section by section ("MEAL COLLECTIONS", "ICED
        COLLECTIONS", ...) with each section's add-ons, so it looks like the
        printed menu.
    HOW:
        1. Loop over CATEGORIES.
        2. Keep only that category's items with a list comprehension:
           `[i for i in menu if i["category"] == category]` (it's a short way to
           write a for loop that builds a list).
        3. If there are items, print the heading, print_addons(category), then
           print_items(items).
    IN THE SYSTEM:
        Menu page option 1, the start of the Order page (and its "Show menu"
        option), and "View all items" in the admin page.
    """
def print_grouped_menu(menu):
    for category in CATEGORIES:
        items = [i for i in menu if i["category"] == category]
        if items:
            print(f"\n{category.upper()} COLLECTIONS")
            print_addons(category)
            print_items(items)


    """
    ASSIGN: __AHRON__
    TASK:
        Shows a numbered list of options and keeps asking until the user picks a
        valid number. Gives back the option that was chosen.
    HOW:
        1. `enumerate(options, start=1)` gives pairs like (1, "Meal"), (2, "Iced").
           Print each one as "  1. Meal".
        2. `while True:` and read a whole number with ask_number(prompt, int, 1).
        3. If it is not bigger than `len(options)`, `return options[picked - 1]`
           (lists start counting at 0, so we subtract 1).
        4. Otherwise print "Please choose 1 to N." and ask again.
    IN THE SYSTEM:
        Used to pick a category (Menu page and add_item) and to pick a size
        (pick_size).
    """
def ask_choice(prompt, options):
    for number, option in enumerate(options, start=1):
        print(f"  {number}. {option}")
    while True:
        picked = ask_number(prompt, int, 1)
        if picked <= len(options):
            return options[picked - 1]
        print(f"  Please choose 1 to {len(options)}.")


# ================================================================ PAGES

    """
    ASSING: __AHRON__
    TASK:
        The customer's Menu page, with a small sub-menu: see the whole menu, browse
        one category, or search by name. Option 0 goes back to the main menu.
    HOW:
        1. `while True:` so the sub-menu keeps showing until the user picks 0.
        2. Print the options and read `choice = input("Choose: ").strip()`.
        3. Use `if / elif / else` on `choice`:
           "1" -> print_grouped_menu(menu)
           "2" -> ask_choice(...) for a category, then print_addons() and
                  print_items() for the items of that category.
           "3" -> ask for a word and show the items where the word is `in` the
                  item name (both in lowercase so "latte" matches "Latte").
           "0" -> `return` (back to the main menu).
           anything else -> "Invalid choice." and `continue`.
        4. Call pause() after showing results.
    IN THE SYSTEM:
        Main menu option 2. This is the Menu page of the website: customers only
        look at items and prices here. Nothing is bought and nothing is saved.
    """
def menu_page(menu):
    while True:
        title("OUR MENU")
        print("1. Whole menu\n2. Browse a category\n3. Search by name\n4. Order\n0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            print_grouped_menu(menu)
        elif choice == "2":
            category = ask_choice("Category number: ", CATEGORIES)
            print(f"\n{category.upper()} COLLECTIONS")
            print_addons(category)
            print_items([i for i in menu if i["category"] == category])
        elif choice == "3":
            term = ask_text("Search: ").lower()
            print_items([i for i in menu if term in i["name"].lower()])
        elif choice == "4":
            orderPage_menu(menu)
        elif choice == "0":
            return
        else:
            print("  Invalid choice.")
            continue
        pause()


    """
    ASSIGN: __ROY__
    TASK:
        The About page: tells the story of Newland's (the text is from the PDF).
    HOW:
        1. title("ABOUT NEWLAND'S").
        2. Loop over ABOUT_PARAGRAPHS. For each one, `print(textwrap.fill(text,
           WIDTH))` (textwrap.fill breaks long text into lines that fit the
           screen), then print() an empty line.
        3. pause().
    IN THE SYSTEM:
        Main menu option 4. It is only text, no data is read or saved. To change
        the story, edit ABOUT_PARAGRAPHS at the top of the file.
    """
def about_page():
    title("ABOUT NEWLAND'S")
    for paragraph in ABOUT_PARAGRAPHS:
        print(textwrap.fill(paragraph, WIDTH))
        print()
    pause()


    """
    ASSIGN: __JEN__
    TASK:
        The Contact page: address, phone, and how to follow the shop.
    HOW:
        1. title("CONTACT US").
        2. print() the address and phone from CONTACT_ADDRESS and CONTACT_PHONE
           (we still need to fill those in at the top of the file).
        3. Tell customers to scan the QR code on the printed menu, then pause().
    IN THE SYSTEM:
        Main menu option 5. Like the "Contact us" page of a website.
    """
def contact_page():
    title("CONTACT US")
    print(f"Address : {CONTACT_ADDRESS}")
    print(f"Phone   : {CONTACT_PHONE}")
    pause()


# ================================================================ ORDERING
# Quick note: our cart is a LIST of "lines". One line looks like this:
#   {"item_id": 38, "size": "12oz", "addons": ["Espresso"], "qty": 2}
# (size is "" for items without sizes, addons is [] when there are none.)


    """
    ASSIGN: __AHRON__
    TASK:
        Price of ONE serving: the base price (for Hot drinks, the price of the
        chosen size) plus the price of every add-on that was picked.
    HOW:
        1. Base price: `item["sizes"][size]` if the item has sizes, else
           `item["price"]`.
        2. Look up each add-on's price in `ADDONS.get(item["category"], {})` and
           add them up with `sum(...)`.
        3. Return base + add-ons.
    IN THE SYSTEM:
        Used for the cart lines, the cart total and the receipt, so the same price
        is used everywhere.
    """
def unit_price(item, size, addons):
    base = item["sizes"][size] if item["sizes"] else item["price"]
    prices = ADDONS.get(item["category"], {})
    return base + sum(prices[name] for name in addons)


    """
    ASSIGN: __AHRON__
    TASK:
        Makes the text of one cart line, like "Latte (12oz) + Espresso" or
        "Tocilog + Extra Rice, Extra Egg".
    HOW:
        Start with `label = item["name"]`. If there is a size, add f" ({size})".
        If there are add-ons, add " + " and then the names joined with ", ".
        Return the label.
    IN THE SYSTEM:
        Used in the cart display, the saved order and the receipt, so the customer
        sees exactly what they ordered.
    """
def line_label(item, size, addons):
    label = item["name"]
    if size:
        label += f" ({size})"
    if addons:
        label += " + " + ", ".join(addons)
    return label


    """
    ASSIGN: __AHRON__
    TASK:
        Counts how many servings of one menu item are already in the cart, counting
        ALL its lines (the same drink can be in the cart in two sizes).
    HOW:
        `sum(l["qty"] for l in cart if l["item_id"] == item_id)` adds up the qty of
        every line that matches.
    IN THE SYSTEM:
        Used by add_to_cart() for the stock check, so a customer can't order more
        than what we have.
    """
def qty_in_cart(cart, item_id):
    return sum(l["qty"] for l in cart if l["item_id"] == item_id)


    """
    ASSIGN: __AHRON__
    TASK:
        Total price of the whole cart.
    HOW:
        For every line: find the item with find_item(), get unit_price(), and
        multiply it by the line's qty. Add everything up with `sum(...)`.
    IN THE SYSTEM:
        Shown at the bottom of the cart, and used at checkout to know how much to
        charge and how much the change is.
    """
def cart_total(menu, cart):
    return sum(unit_price(find_item(menu, l["item_id"]), l["size"], l["addons"])
               * l["qty"] for l in cart)



    """
    ASSIGN: __ROY__
    TASK:
        Prints the cart with line numbers (so the customer can remove a line), the
        amount of each line, and the grand total. Shows "(empty)" when there's
        nothing yet.
    HOW:
        1. Print the "YOUR CART" heading and a divider.
        2. `if not cart:` print "(empty)" and `return`.
        3. `for number, l in enumerate(cart, start=1):` find the item, build the
           label with line_label(), print "number. qty x label", then print the
           amount on the right with f"{amount:>{WIDTH}.2f}".
        4. Print a divider and the grand total from cart_total().
    IN THE SYSTEM:
        The Order page shows it every time before the options, so the customer
        always sees what is in their order so far.
    """
def show_cart(menu, cart):
    print("\nYOUR CART")
    line()
    if not cart:
        print("  (empty)")
        return
    for number, l in enumerate(cart, start=1):
        item = find_item(menu, l["item_id"])
        amount = unit_price(item, l["size"], l["addons"]) * l["qty"]
        print(f"  {number}. {l['qty']} x {line_label(item, l['size'], l['addons'])}")
        print(f"{amount:>{WIDTH}.2f}")
    line()
    print(f"  TOTAL{cart_total(menu, cart):>{WIDTH - 7}.2f}")


    """
    ASSIGN: __AHRON__
    TASK:
        Prints the receipt of a finished order: order number, date, customer, every
        line, then total, amount paid and change.
    HOW:
        1. title(...) with the shop name, then the order number
           (`{order['order_no']:04d}` pads it like 0007), the date and the
           customer name.
        2. Loop over `order["items"]`, print "qty x label" and the line amount
           (price * qty) on the right.
        3. Print total, paid and change with the same alignment, then a thank-you
           message.
    IN THE SYSTEM:
        Called by checkout() right after the order is saved. It is the last thing
        the customer sees when they order.
    """
def print_receipt(order):
    title(f"{SHOP_NAME.upper()} - RECEIPT")
    print(f"Order #{order['order_no']:04d}    {order['date']}")
    print(f"Customer: {order['customer']}")
    line()
    for it in order["items"]:
        print(f"  {it['qty']} x {it['label']}")
        print(f"{it['price'] * it['qty']:>{WIDTH}.2f}")
    line()
    print(f"  Total{order['total']:>{WIDTH - 7}.2f}")
    print(f"  Paid{order['paid']:>{WIDTH - 6}.2f}")
    print(f"  Change{order['change']:>{WIDTH - 8}.2f}")
    print("\nThank you for supporting our student baristas!")


    """
    ASSIGN: __ROY__
    TASK:
        Finishes an order: takes the payment, subtracts the sold quantities from
        stock, saves the order history and prints the receipt. Gives back True if
        the order was completed, False if the cart was empty.
    HOW:
        1. If the cart is empty, print a message and `return False`.
        2. Get the total with cart_total(), then ask for the customer's name.
        3. Ask for the amount paid with ask_number(..., float, 0) inside a
           `while True:` loop. Only `break` when paid >= total.
        4. For each cart line: subtract its qty from `item["stock"]` and add
           {"name", "label", "qty", "price"} (price = unit_price) to a list called
           `items`.
        5. save_json(MENU_FILE, menu) so the new stock numbers are kept.
        6. Load the old orders with load_json(ORDERS_FILE, []). Build the new order
           dict (order_no = number of old orders + 1, the date from
           `datetime.now().strftime(...)`, change = paid - total), append it, and
           save_json(ORDERS_FILE, orders).
        7. print_receipt(order) and `return True`.
    IN THE SYSTEM:
        Called by order_page() (option 4). I think this is the most important
        function: it connects ordering, stock tracking and sales history. It lowers
        the stock in the menu file and adds a new record to the orders file, which
        the sales report reads later.
    """
def checkout(menu, cart):
    if not cart:
        print("  Your cart is empty.")
        return False
    total = cart_total(menu, cart)
    customer = ask_text("Customer name: ")
    print(f"Total due: {money(total)}")
    while True:
        paid = ask_number("Amount paid: PHP ", float, 0)
        if paid >= total:
            break
        print("  Not enough. Please pay at least the total.")
    items = []
    for l in cart:
        item = find_item(menu, l["item_id"])
        item["stock"] -= l["qty"]
        items.append({"name": item["name"],
                      "label": line_label(item, l["size"], l["addons"]),
                      "qty": l["qty"],
                      "price": unit_price(item, l["size"], l["addons"])})
    save_json(MENU_FILE, menu)
    orders = load_json(ORDERS_FILE, [])
    order = {
        "order_no": len(orders) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "customer": customer,
        "items": items,
        "total": total,
        "paid": paid,
        "change": paid - total,
    }
    orders.append(order)
    save_json(ORDERS_FILE, orders)
    print_receipt(order)
    return True


    """
    ASSIGN: __AHRON__
    TASK:
        For Hot drinks, asks which size the customer wants (8oz or 12oz). Items
        without sizes need no question, so it gives back "".
    HOW:
        1. `if not item["sizes"]:` `return ""`.
        2. Otherwise `return ask_choice("Size number: ", list(item["sizes"]))`.
           `list(dict)` gives just the keys: ["8oz", "12oz"].
    IN THE SYSTEM:
        Called by add_to_cart(). The size the customer picks decides the price in
        unit_price().
    """
def pick_size(item):
    if not item["sizes"]:
        return ""
    return ask_choice("Size number: ", list(item["sizes"]))


    """
    ASSIGN: __AHRON__
    TASK:
        Asks which add-ons the customer wants, using the add-ons of the item's
        category (see ADDONS). Gives back a list of add-on names ([] for none).
        The customer types numbers like "1,2", or just presses Enter.
    HOW:
        1. `available = ADDONS.get(item["category"], {})`. If it is empty,
           `return []`. Then `names = list(available)`.
        2. Loop with `while True:`. Print each add-on with its number and price,
           then read the answer with input().
        3. Empty answer -> `return []`.
        4. Otherwise remove the spaces and split on commas:
           `parts = raw.replace(" ", "").split(",")`.
        5. Check that EVERY part is a digit from 1 up to len(names). `all(...)` is
           True only when every check passes. If it's valid, change the numbers
           into names. `dict.fromkeys(parts)` removes duplicates like "1,1" and
           keeps the order.
        6. If something is invalid, print a hint and ask again.
    IN THE SYSTEM:
        Called by add_to_cart(). The add-ons picked here are added to the price in
        unit_price() and shown in the cart and receipt.
    """
def pick_addons(item):
    available = ADDONS.get(item["category"], {})
    if not available:
        return []
    names = list(available)
    while True:
        for number, name in enumerate(names, start=1):
            print(f"  {number}. {name} +{available[name]}")
        raw = input("Add-ons (like 1,2) or Enter for none: ").strip()
        if raw == "":
            return []
        parts = [p for p in raw.replace(" ", "").split(",") if p]
        if parts and all(p.isdigit() and 1 <= int(p) <= len(names) for p in parts):
            return [names[int(p) - 1] for p in dict.fromkeys(parts)]
        print("  Please type numbers from the list, like 1,2.")


    """
    TASK:
        If two cart lines are exactly the same (same item, same size, same
        add-ons), combine them into one line and add their quantities. Without
        this, ordering the same drink twice would show up as 2 lines.
    HOW:
        1. Start a new empty list `merged = []`.
        2. For every line in the cart, look through `merged` for a line with the
           same item_id, size and addons. If we find one, add the qty to it and
           `break`.
        3. The `else:` of the inner `for` runs only when there was NO break (no
           match), so then we append the line as a new one.
        4. `cart[:] = merged` replaces the CONTENTS of the same list, so
           order_page() still sees the updated cart.
    IN THE SYSTEM:
        Called by add_to_cart() and change_options() to keep the cart short and
        neat. The total price stays the same, only the lines change.
    """
def merge_same_lines(cart):
    merged = []
    for entry in cart:
        for m in merged:
            if (m["item_id"], m["size"], m["addons"]) == \
                    (entry["item_id"], entry["size"], entry["addons"]):
                m["qty"] += entry["qty"]
                break
        else:
            merged.append(entry)
    cart[:] = merged
    
    """
    ASSIGN: __AHRON__
    TASK:
        Adds one line to the cart: item, size (if any), add-ons and quantity. The
        cart must never hold more of an item than we have in stock.
    HOW:
        1. Ask for the item id and find it with find_item(). If it is None or its
           stock is 0, print "not available" and `return`.
        2. Call pick_size(item) and pick_addons(item), then ask the quantity with
           ask_number(..., int, 1).
        3. Stock check: `already = qty_in_cart(cart, item["id"])`. If
           `already + qty > item["stock"]`, print how many more are available
           (`item["stock"] - already`) and `return`.
        4. Otherwise `cart.append({...})` the new line. (The cart is a list that
           lives in order_page(), so appending here changes it there too.)
    IN THE SYSTEM:
        Order page option 1. It is where the customer builds their order. Stock is
        only checked here and NOT lowered yet - that happens in checkout().
    """
def add_to_cart(menu, cart):
    item = find_item(menu, ask_number("Item ID: ", int, 1))
    if not item or item["stock"] == 0:
        print("  That item is not available.")
        return
    size = pick_size(item)
    addons = pick_addons(item)
    qty = ask_number("Quantity: ", int, 1)
    already = qty_in_cart(cart, item["id"])
    if already + qty > item["stock"]:
        print(f"  Sorry, only {item['stock'] - already} more available.")
        return
    cart.append({"item_id": item["id"], "size": size, "addons": addons, "qty": qty})
    print("  Added to cart.")

    """
    TASK:
        Asks the customer for ONE cart line number (the numbers shown by
        show_cart) and keeps asking until it is a real line. Pressing Enter
        cancels and gives back None.
    HOW:
        1. `while True:` and read the number with ask_number(..., int, 1, True).
           The last True lets the customer press Enter to cancel.
        2. If it is None, `return None`.
        3. If it is not bigger than `len(cart)`, `return number`.
        4. Otherwise print "Please choose a line from 1 to N." and ask again.
    IN THE SYSTEM:
        Used by change_quantity() and change_options() so both ask for the line
        the same way.
    """
def ask_line_number(cart, prompt):
    while True:
        number = ask_number(prompt + " (Enter to cancel): ", int, 1, True)
        if number is None:
            return None
        if number <= len(cart):
            return number
        print(f"  Please choose a line from 1 to {len(cart)}.")


    """
    TASK:
        Asks for ONE OR MORE cart line numbers, like "2" or "1,3", so the
        customer can pick several lines at once. Gives back a sorted list of
        numbers ([] if the customer cancels).
    HOW:
        1. `while True:` and read `raw = input(...)`. An empty answer means
           cancel, so `return []`.
        2. Remove the spaces and split on commas (same trick as pick_addons()).
        3. If EVERY part is a digit from 1 up to len(cart), return
           `sorted({int(p) for p in parts})` (a set removes duplicates).
        4. Otherwise print a hint and ask again.
    IN THE SYSTEM:
        Used by delete_from_cart() so the customer can delete many items in one go.
    """
def ask_line_numbers(cart, prompt):
    while True:
        raw = input(prompt + " (like 2 or 1,3, Enter to cancel): ").strip()
        if raw == "":
            return []
        parts = [p for p in raw.replace(" ", "").split(",") if p]
        if parts and all(p.isdigit() and 1 <= int(p) <= len(cart) for p in parts):
            return sorted({int(p) for p in parts})
        print(f"  Please type line numbers from 1 to {len(cart)}, like 1,3.")


    """
    TASK:
        Lets the customer change the quantity of one cart line: add more or
        reduce it. The new quantity can't be more than the stock we have.
    HOW:
        1. Ask which line with ask_line_number(). If None, `return`.
        2. Get the line `entry = cart[number - 1]` and its item with find_item().
        3. Work out how many we can still sell: the same item may be in other
           lines too, so `others = qty_in_cart(...) - entry["qty"]` and
           `room = item["stock"] - others`.
        4. Ask the new quantity with ask_number(..., int, 1). If it is bigger than
           `room`, print how many are available and `return`.
        5. Otherwise save it: `entry["qty"] = new_qty`.
    IN THE SYSTEM:
        Edit cart option 1. It is the "add quantity" part of editing, and it
        uses the same stock rule as add_to_cart() so we never oversell.
    """
def change_quantity(menu, cart):
    number = ask_line_number(cart, "Which line number?")
    if number is None:
        return
    entry = cart[number - 1]
    item = find_item(menu, entry["item_id"])
    others = qty_in_cart(cart, item["id"]) - entry["qty"]
    room = item["stock"] - others
    print(f"  Now: {entry['qty']} x {line_label(item, entry['size'], entry['addons'])}"
          f"  (up to {room} available)")
    new_qty = ask_number("New quantity: ", int, 1)
    if new_qty > room:
        print(f"  Sorry, only {room} available.")
        return
    entry["qty"] = new_qty
    print("  Quantity updated.")



    """
    TASK:
        Lets the customer change the size and the add-ons of one cart line
        (for example 8oz to 12oz, or add an Espresso shot).
    HOW:
        1. Ask which line with ask_line_number(). If None, `return`.
        2. Find its item. If the item has no sizes AND its category has no
           add-ons (like Brewed), print a message and `return`.
        3. Show what the line is now with line_label().
        4. Ask again with pick_size(item) and pick_addons(item) and save them in
           the line. The add-ons you pick REPLACE the old ones, and pressing
           Enter means no add-ons.
        5. Call merge_same_lines(cart) in case the line now matches another one.
    IN THE SYSTEM:
        Edit cart option 2. The price updates by itself because show_cart() and
        cart_total() always use unit_price() with the line's current size and
        add-ons.
    """
def change_options(menu, cart):
    number = ask_line_number(cart, "Which line number?")
    if number is None:
        return
    entry = cart[number - 1]
    item = find_item(menu, entry["item_id"])
    if not item["sizes"] and not ADDONS.get(item["category"]):
        print("  This item has no sizes or add-ons to change.")
        return
    print(f"  Now: {line_label(item, entry['size'], entry['addons'])}")
    entry["size"] = pick_size(item)
    entry["addons"] = pick_addons(item)
    merge_same_lines(cart)
    print("  Item updated.")

    """
    TASK:
        Deletes the chosen line(s) from the cart. The customer can type one line
        number or several, like "1,3".
    HOW:
        1. Ask with ask_line_numbers(cart, ...). If the answer is empty, `return`.
        2. Delete from the BIGGEST number to the smallest:
           `for n in reversed(numbers): cart.pop(n - 1)`. If we deleted line 1
           first, the other lines would move up and we'd delete the wrong ones!
        3. Print how many lines were deleted.
    IN THE SYSTEM:
        Edit cart option 3. It is for when the customer changes their mind before
        paying. Nothing is saved to the files until checkout().
    """
def delete_from_cart(cart):
    numbers = ask_line_numbers(cart, "Line number(s) to delete")
    if not numbers:
        return
    for n in reversed(numbers):
        cart.pop(n - 1)
    print(f"  Deleted {len(numbers)} line(s).")


    """
    TASK:
        The "Edit cart" screen. From here the customer can change a quantity,
        change the size / add-ons, or delete items, then go back to ordering.
    HOW:
        1. If the cart is empty, print a message and `return`.
        2. Loop with `while True:`. Each time show the cart with show_cart() and
           the options: 1 Change quantity, 2 Change size / add-ons, 3 Delete
           item(s), 0 Back.
        3. Send each choice to its function: change_quantity, change_options,
           delete_from_cart.
        4. After an action, if the cart became empty (everything was deleted),
           print a message and `return`.
        5. Option 0: `return` to the order page.
    IN THE SYSTEM:
        Order page option 2. It changes the same `cart` list that checkout() uses
        later, so whatever the customer edits here is exactly what they pay for.
    """
def edit_cart(menu, cart):
    if not cart:
        print("  Your cart is empty, so there is nothing to edit.")
        return
    while True:
        show_cart(menu, cart)
        print("\nEDIT CART")
        print("1. Change quantity (add or reduce)\n2. Change size / add-ons")
        print("3. Delete item(s)\n0. Back to ordering")
        choice = input("Choose: ").strip()
        if choice == "1":
            change_quantity(menu, cart)
        elif choice == "2":
            change_options(menu, cart)
        elif choice == "3":
            delete_from_cart(cart)
        elif choice == "0":
            return
        else:
            print("  Invalid choice.")
        if not cart:
            print("  Your cart is now empty.")
            return


    """
    ASSIGN: __ROY__
    TASK:
        The ordering system. The customer builds a cart (add / remove lines), can
        look at the menu again, then checks out.
    HOW:
        1. Make an empty list `cart = []` and print the whole menu once with
           print_grouped_menu(menu), so the customer can see the item ids.
        2. Loop with `while True:`. Each time show the cart with show_cart() and
           the options: 1 Add, 2 Remove, 3 Show menu, 4 Checkout, 0 Cancel.
        3. Send each choice to its function: add_to_cart, remove_from_cart,
           print_grouped_menu.
        4. Option 4: if `checkout(menu, cart)` returns True, call pause() and
           `return`.
        5. Option 0: `return` (cancel the order).
    IN THE SYSTEM:
        Main menu option 3. This is the ordering part of our website. The cart only
        lives while the customer is ordering. Stock and sales history change only
        when checkout() finishes.
    """
def order_page(menu):
    cart = []
    title("PLACE AN ORDER")
    print_grouped_menu(menu)
    while True:
        show_cart(menu, cart)
        print("\n1. Add item\n2. Remove item\n3. Edit cart\n4. Search item\n5. Checkout\n0. Cancel order")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_to_cart(menu, cart)
        elif choice == "2":
            delete_from_cart(cart)
        elif choice == "3":
            edit_cart(menu, cart)
        elif choice == "4":
            term = ask_text("Search: ").lower()
            print_items([i for i in menu if term in i["name"].lower()]) 
        elif choice == "5":
            if checkout(menu, cart):
                pause()
                return
        elif choice == "0":
            return main()
        else:
            print("  Invalid choice.")

"""This is a modified version of the order_page function
     that allows customers to search for items by name instead of showing 
     the whole menu again. It also includes an option to cancel the order and return to the main menu."""
def orderPage_menu(menu):
    cart = []
    title("PLACE AN ORDER")
    while True:
        show_cart(menu, cart)
        print("\n1. Add item\n2. Remove item\n3. Edit cart\n4. Search item\n5. Checkout\n0. Cancel order")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_to_cart(menu, cart)
        elif choice == "2":
            delete_from_cart(cart)
        elif choice == "3":
            edit_cart(menu, cart)
        elif choice == "4":
            term = ask_text("Search: ").lower()
            print_items([i for i in menu if term in i["name"].lower()])
        elif choice == "5":
            if checkout(menu, cart):
                pause()
                return
        elif choice == "0":
            return
        else:
            print("  Invalid choice.")


# ================================================================ ADMIN

    """
    ASSIGN: __AHRON__
    TASK:
        Adds a brand-new item to the menu with a starting stock. Two items must not
        have the same name.
    HOW:
        1. Ask for the name with ask_text. Duplicate check:
           `any(i["name"].lower() == name.lower() for i in menu)` is True if the
           name already exists. Then print a message and `return`.
        2. Pick the category with ask_choice("Category number: ", CATEGORIES).
        3. Price: if the category is "Hot", ask one price per size (loop over
           SIZES) and keep them in a dict. Otherwise ask one price with
           ask_number(..., float, 0.01).
        4. Ask for an optional description (blank allowed) and the starting stock.
        5. `menu.append({...})` a dict with id=next_id(menu) and the same keys that
           build_default_menu() uses, then save_json(MENU_FILE, menu).
    IN THE SYSTEM:
        Admin option 2. The new item shows up right away on the Menu and Order
        pages because all the pages share the same `menu` list.
    """
def add_item(menu):
    name = ask_text("Name: ")
    if any(i["name"].lower() == name.lower() for i in menu):
        print("  That item already exists.")
        return
    category = ask_choice("Category number: ", CATEGORIES)
    sizes = {}
    if category == "Hot":
        for size in SIZES:
            sizes[size] = ask_number(f"Price for {size}: PHP ", float, 0.01)
        price = sizes[SIZES[0]]
    else:
        price = ask_number("Price: PHP ", float, 0.01)
    note = ask_text("Short description (optional): ", True)
    stock = ask_number("Starting stock: ", int, 0)
    menu.append({"id": next_id(menu), "name": name, "category": category,
                 "price": price, "sizes": sizes, "note": note, "stock": stock})
    save_json(MENU_FILE, menu)
    print("  Item added.")


    """
    ASSIGN: __AHRON__
    TASK:
        Changes an existing item's name, price (or prices, for Hot drinks) or
        description. Pressing Enter on a question keeps the old value.
    HOW:
        1. Ask for the item id and find it with find_item(). If None, print "Item
           not found." and `return`.
        2. Name and description: use ask_text(..., True) (blank allowed) with the
           trick `new_value or old_value`. An empty string counts as False, so the
           old value is kept.
        3. Prices: if the item has sizes, loop over `item["sizes"]` and ask the new
           price of each size with ask_number(..., float, 0.01, True). It gives
           None when blank, so only change it `if new is not None`. Then set
           `item["price"]` to the first size's price. Without sizes, ask for the
           single price the same way.
        4. save_json(MENU_FILE, menu) and print "Item updated."
    IN THE SYSTEM:
        Admin option 3. Use it when a price on the menu changes or there's a typo
        in a name. Customers see the new details immediately.
    """
def edit_item(menu):
    item = find_item(menu, ask_number("Item ID to edit: ", int, 1))
    if not item:
        print("  Item not found.")
        return
    print("Leave blank to keep the current value.")
    item["name"] = ask_text(f"Name [{item['name']}]: ", True) or item["name"]
    item["note"] = ask_text("Description (Enter to keep): ", True) or item["note"]
    if item["sizes"]:
        for size in item["sizes"]:
            new = ask_number(f"{size} price [{item['sizes'][size]:g}]: PHP ",
                             float, 0.01, True)
            if new is not None:
                item["sizes"][size] = new
        item["price"] = list(item["sizes"].values())[0]
    else:
        new = ask_number(f"Price [{item['price']:g}]: PHP ", float, 0.01, True)
        if new is not None:
            item["price"] = new
    save_json(MENU_FILE, menu)
    print("  Item updated.")


    """
    ASSIGN: __AHRON__
    TASK:
        Stock tracking: adds newly delivered stock to an item (like 20 more Tocilog
        portions are ready).
    HOW:
        1. Ask for the item id and find_item(). If None, print a message and
           `return`.
        2. Ask how many to add with ask_number(..., int, 1) (at least 1).
        3. Add it: `item["stock"] += qty` (it's the same as stock = stock + qty).
        4. save_json(MENU_FILE, menu) and print the new stock level.
    IN THE SYSTEM:
        Admin option 4. Stock goes DOWN in checkout() and goes UP here, so together
        they keep the numbers correct.
    """
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
    ASSIGN: __AHRON__
    TASK:
        Removes an item from the menu, but only after the admin confirms, so
        nothing gets deleted by accident.
    HOW:
        1. Ask for the item id and find_item(). If None, print a message and
           `return`.
        2. Ask "Delete <name>? (y/n)" and compare the answer (in lowercase) with "y".
        3. If yes: `menu.remove(item)`, then save_json(MENU_FILE, menu) and print
           "Item deleted." If no, do nothing.
    IN THE SYSTEM:
        Admin option 5. For items the shop doesn't sell anymore. Old orders keep
        their item names, so the sales report still works.
    """
def delete_item(menu):
    item = find_item(menu, ask_number("Item ID to delete: ", int, 1))
    if not item:
        print("  Item not found.")
        return
    if input(f"Delete {item['name']}? (y/n): ").strip().lower() == "y":
        menu.remove(item)
        save_json(MENU_FILE, menu)
        print("  Item deleted.")


    """
    ASSIGN: __AHRON__
    TASK:
        Puts the menu back to the original Newland's menu from the PDF (every stock
        goes back to DEFAULT_STOCK). Useful if the data gets messy while we test.
    HOW:
        1. Ask for confirmation (y/n) because this erases all menu changes.
        2. If yes: `menu[:] = build_default_menu()`. The `[:]` replaces the CONTENTS
           of the same list instead of making a new list, so every page that has
           this `menu` sees the change.
        3. save_json(MENU_FILE, menu) and print a message.
    IN THE SYSTEM:
        Admin option 8. Mostly for testing, or for starting a new day with fresh
        stock. It does not delete the saved orders.
    """
def reset_menu(menu):
    answer = input("Reset the whole menu and all stock? (y/n): ").strip().lower()
    if answer == "y":
        menu[:] = build_default_menu()
        save_json(MENU_FILE, menu)
        print("  Menu reset to the original Newland's menu.")


    """
    ASSIGN: __ROY__
    TASK:
        Shows the items that are sold out or running low, so the admin knows what to
        restock. "Low" means LOW_STOCK (5) or fewer.
    HOW:
        Build a filtered list with a list comprehension,
        `[i for i in menu if i["stock"] <= LOW_STOCK]`, and show it with
        print_items().
    IN THE SYSTEM:
        Admin option 6. It helps the admin decide what to restock with option 4.
    """
def low_stock_report(menu):
    print(f"\nItems with {LOW_STOCK} or fewer in stock:")
    print_items([i for i in menu if i["stock"] <= LOW_STOCK])


    """
    ASSIGN: __ROY__
    TASK:
        Summarizes the sales: number of orders, total revenue and the top 3
        best-selling items.
    HOW:
        1. `orders = load_json(ORDERS_FILE, [])`. If it is empty, print "No orders
           yet." and `return`.
        2. Make `sold = Counter()`. A Counter is a dict that counts things for us.
        3. Loop over every order and every item in it and add the quantity:
           `sold[it["name"]] += it["qty"]`.
        4. Revenue = `sum(o["total"] for o in orders)`.
        5. `sold.most_common(3)` gives the 3 biggest sellers as (name, qty) pairs.
    IN THE SYSTEM:
        Admin option 7. It reads the orders that checkout() saved, so it only shows
        something after at least one order is finished.
    """
def sales_report():
    orders = load_json(ORDERS_FILE, [])
    if not orders:
        print("  No orders yet.")
        return
    sold = Counter()
    for o in orders:
        for it in o["items"]:
            sold[it["name"]] += it["qty"]
    print(f"\nTotal orders : {len(orders)}")
    print(f"Total revenue: {money(sum(o['total'] for o in orders))}")
    print("Best sellers :")
    for name, qty in sold.most_common(3):
        print(f"  {name}: {qty} sold")


    """
    ASSIGN: __AHRON__
    TASK:
        The menu-management console. It is protected by a PIN and lets the admin
        view, add, edit, restock and delete items, reset the menu and see the
        reports.
    HOW:
        1. PIN check: `for _ in range(3):` gives 3 tries. If the typed PIN equals
           ADMIN_PIN, `break`. The `else:` attached to the `for` runs only when the
           loop finished without a break. Then print "Too many attempts." and
           `return`.
        2. Make a dict `actions` that matches each choice ("2", "3", ...) to the
           function to run. `lambda: add_item(menu)` wraps a function call so it
           runs later, only when that choice is picked.
        3. Loop with `while True:`, print the options and read the choice.
        4. "0" -> `return`. "1" -> print_grouped_menu(menu). A choice found in
           `actions` -> call it with `actions[choice]()`. Anything else -> print
           "Invalid choice." and `continue`.
        5. Call pause() after each action.
    IN THE SYSTEM:
        Main menu option 6. This is the Manage page of the website. Only the staff
        should get in, which is why we ask for the PIN first.
    """
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
        "8": lambda: reset_menu(menu),
    }
    while True:
        title("MENU MANAGEMENT")
        print("1. View all items   2. Add item      3. Edit item")
        print("4. Restock item     5. Delete item   6. Low stock report")
        print("7. Sales report     8. Reset menu    0. Back")
        choice = input("Choose: ").strip()
        if choice == "0":
            return
        if choice == "1":
            print_grouped_menu(menu)
        elif choice in actions:
            actions[choice]()
        else:
            print("  Invalid choice.")
            continue
        pause()


# ================================================================ MAIN
    """
    ASSIGN: __AHRON__
    TASK:
        Starts the program: loads the menu (or builds the Newland's menu on the very
        first run) and keeps showing the main menu until the user exits.
    HOW:
        1. `menu = load_json(MENU_FILE, None)`. If it is None (no file yet), use
           build_default_menu() and save it with save_json().
        2. Loop with `while True:`, print the options and read the choice.
        3. Send each choice to its page function (home_page, menu_page, order_page,
           about_page, contact_page, admin_page).
        4. "0" prints "Goodbye!" and `return`, which ends the program.
        5. Always pass the SAME `menu` list to the pages. They change it in place,
           so every page sees the latest stock.
    IN THE SYSTEM:
        This is where the program begins (see the last lines of the file). Every
        other function is reached from here, so it works like the navigation bar
        of our website.
    """
def main():
    menu = load_json(MENU_FILE, None)
    if menu is None:
        menu = build_default_menu()
        save_json(MENU_FILE, menu)
    while True:
        title(f"WELCOME TO {SHOP_NAME.upper()}")
        print("1. Menu\n2. Order\n3. About us\n4. Contact us")
        print("5. Menu management (admin)\n0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            menu_page(menu)
        elif choice == "2":
            order_page(menu)
        elif choice == "3":
            about_page()
        elif choice == "4":
            contact_page()
        elif choice == "5":
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