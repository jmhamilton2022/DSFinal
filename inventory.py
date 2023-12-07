import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, ttk


# class to represent a product in inventory
class Product:
    def __init__(self, product_id, name, quantity, expiry_date=None):
        self.product_id = product_id
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date

    def __str__(self):
        expiry_info = f"Expires on: {self.expiry_date}" if self.expiry_date else "No expiry date"
        return f"{self.name} - {self.quantity} left. {expiry_info}"


# List to store products in the stockroom
stock_room = []

# dictionary for product lookup
product_lookup = {}

# queue as list to track low items
queue = []

# constant to set low stock number
LOW_STOCK_THRESHOLD = 10


# add a new item
def add_product(product):
    stock_room.append(product)
    product_lookup[product.product_id] = product
    check_and_alert_low_stock()


# remove an item
def remove_product(product_id):
    product = product_lookup[product_id]
    stock_room.remove(product)
    del product_lookup[product_id]
    if product in queue:
        queue.remove(product)
    check_and_alert_low_stock()


# update values in the combobox with current items
def update_combobox():
    product_names = [product.name for product in stock_room]
    combobox['values'] = product_names


# update the quantity of an item
def update_quantity(product_id, delta):
    product = product_lookup[product_id]
    product.quantity += delta

    # add or remove items from low stock queue
    if product.quantity < LOW_STOCK_THRESHOLD and product not in queue:
        queue.append(product)
    elif product.quantity >= LOW_STOCK_THRESHOLD and product in queue:
        queue.remove(product)

    check_and_alert_low_stock()


# check for low stock and tell me about it
def check_and_alert_low_stock():
    if queue:
        low_stock_items = ", ".join([prod.name for prod in queue])
        messagebox.showwarning("Low Stock Alert", f"The following items are low on stock: {low_stock_items}")


# sort items in inventory by quantity
def insertion_sort(array):
    for i in range(1, len(array)):
        key_item = array[i]
        j = i - 1
        while j >= 0 and array[j].quantity > key_item.quantity:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key_item
    return array


# input to add an item
def add_product_gui():
    product_id = simpledialog.askstring("Input", "Enter product ID:")
    name = simpledialog.askstring("Input", "Enter product name:")
    quantity = simpledialog.askinteger("Input", "Enter product quantity:")
    expiry_date = simpledialog.askstring("Input", "Enter expiry date (optional):")

    if not product_id or not name or quantity is None:
        messagebox.showerror("Error", "Please provide all required information!")
        return

    product = Product(product_id, name, quantity, expiry_date)
    add_product(product)
    update_listbox()
    update_combobox()


# input to remove an item
def remove_product_gui():
    product_id = simpledialog.askstring("Input", "Enter product ID to remove:")

    if not product_id or product_id not in product_lookup:
        messagebox.showerror("Error", "Invalid product ID!")
        return

    remove_product(product_id)
    update_listbox()
    update_combobox()


# update the quantity
def update_quantity_gui():
    selected_product_name = combobox.get()
    product_id = None

    for prod_id, prod in product_lookup.items():
        if prod.name == selected_product_name:
            product_id = prod_id
            break

    if not product_id:
        messagebox.showerror("Error", "Please select a valid product!")
        return

    delta = simpledialog.askinteger("Input", "Enter quantity change (can be negative):")
    if delta is None:
        return

    update_quantity(product_id, delta)
    update_listbox()
    update_combobox()


# update the listbox with sorted products
def update_listbox():
    listbox.delete(0, tk.END)
    sorted_products = insertion_sort(stock_room)
    for product in sorted_products:
        listbox.insert(tk.END, product)
        if product.quantity < LOW_STOCK_THRESHOLD:
            listbox.itemconfig(tk.END, {'bg': 'red'})


if __name__ == '__main__':

    # Main GUI
    root = tk.Tk()
    root.title("Inventory Management")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    btn_add = tk.Button(frame, text="Add Product", command=add_product_gui)
    btn_add.pack(fill=tk.X)

    btn_remove = tk.Button(frame, text="Remove Product", command=remove_product_gui)
    btn_remove.pack(fill=tk.X, pady=(5, 0))

    btn_update = tk.Button(frame, text="Update Quantity", command=update_quantity_gui)
    btn_update.pack(fill=tk.X, pady=(5, 0))

    listbox = Listbox(frame, height=15, width=50)
    listbox.pack(pady=(10, 0))

    combobox_label = tk.Label(frame, text="Select a Product to Update")
    combobox_label.pack(pady=(5, 0))

    combobox = ttk.Combobox(frame, state="readonly")
    combobox.pack(pady=(5, 0))

    root.mainloop()
