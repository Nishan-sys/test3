import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a database if it doesn't exist
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory
    (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER)
''')
conn.commit()
conn.close()

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Control System")
        self.root.geometry("400x300")

        # Frames
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(pady=10)

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(pady=10)

        self.frame3 = tk.Frame(self.root)
        self.frame3.pack(pady=10)

        # Labels and Entries
        tk.Label(self.frame1, text="Item Name").pack(side=tk.LEFT)
        self.name_entry = tk.Entry(self.frame1)
        self.name_entry.pack(side=tk.LEFT)

        tk.Label(self.frame2, text="Quantity").pack(side=tk.LEFT)
        self.quantity_entry = tk.Entry(self.frame2)
        self.quantity_entry.pack(side=tk.LEFT)

        # Buttons
        self.add_button = tk.Button(self.frame3, text="Add Item", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.frame3, text="Remove Item", command=self.remove_item)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.view_button = tk.Button(self.frame3, text="View Inventory", command=self.view_inventory)
        self.view_button.pack(side=tk.LEFT, padx=5)

    def add_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        
        if name and quantity:
            try:
                quantity = int(quantity)
                conn = sqlite3.connect('inventory.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO inventory (name, quantity) VALUES (?, ?)', (name, quantity))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Item added successfully.")
                self.name_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Quantity must be an integer.")
        else:
            messagebox.showerror("Error", "Please fill in both fields.")

    def remove_item(self):
        name = self.name_entry.get()
        if name:
            conn = sqlite3.connect('inventory.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM inventory WHERE name = ?', (name,))
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Item removed successfully.")
                self.name_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Item not found in inventory.")
                conn.close()
        else:
            messagebox.showerror("Error", "Please enter the item name.")

    def view_inventory(self):
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM inventory')
        rows = cursor.fetchall()
        conn.close()

        if rows:
            inventory_window = tk.Toplevel(self.root)
            inventory_window.title("Current Inventory")
            text_area = tk.Text(inventory_window, width=50, height=10)
            text_area.pack()
            for row in rows:
                text_area.insert(tk.END, f"ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}\n")
        else:
            messagebox.showinfo("Inventory", "No items in inventory.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystem(root)
    root.mainloop()
