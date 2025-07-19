import tkinter as tk
from tkinter import ttk, messagebox

class ContactBookUI:
    def __init__(self, master, app_controller):
        
        self.master = master
        master.title("Python Contact Book")
        master.geometry("800x600") # Set initial window size
        master.resizable(True, True) # Allow window resizing

        self.app_controller = app_controller

        self.style = ttk.Style()
        self.style.theme_use('clam') 
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Inter', 10))
        self.style.configure('TButton', font=('Inter', 10, 'bold'), padding=6, borderwidth=2, relief="raised")
        self.style.map('TButton',
                       background=[('active', '#e0e0e0')],
                       foreground=[('active', 'black')])
        self.style.configure('Treeview.Heading', font=('Inter', 10, 'bold'))
        self.style.configure('Treeview', font=('Inter', 10), rowheight=25)

        self.create_widgets()
        self.refresh_contact_list() # Load contacts on startup

    def create_widgets(self):
        """
        Creates and lays out all the GUI widgets.
        """
        # --- Main Frame ---
        main_frame = ttk.Frame(self.master, padding="15 15 15 15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Frame (for Add/Update) ---
        input_frame = ttk.LabelFrame(main_frame, text="Contact Details", padding="10 10 10 10")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Labels and Entry fields for contact details
        labels = ['Name:', 'Phone:', 'Email:', 'Address:']
        self.entries = {} # Store entry widgets for easy access
        for i, text in enumerate(labels):
            ttk.Label(input_frame, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(input_frame, width=40)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entries[text.replace(':', '').strip().lower().replace(' ', '_')] = entry

        # Configure column weights for input frame
        input_frame.grid_columnconfigure(1, weight=1)

        # --- Action Buttons Frame ---
        button_frame = ttk.Frame(main_frame, padding="5 0 5 0")
        button_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        ttk.Button(button_frame, text="Add Contact", command=self.add_contact).pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="Update Contact", command=self.update_contact).pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        ttk.Button(button_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

        # --- Search Frame ---
        search_frame = ttk.LabelFrame(main_frame, text="Search Contacts", padding="10 10 10 10")
        search_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(search_frame, text="Search Query:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.search_by_var = tk.StringVar(value="phone") # Default search by phone
        ttk.Radiobutton(search_frame, text="By Phone", variable=self.search_by_var, value="phone").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        ttk.Radiobutton(search_frame, text="By Name", variable=self.search_by_var, value="name").grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Button(search_frame, text="Search", command=self.search_contacts).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        ttk.Button(search_frame, text="Show All", command=self.refresh_contact_list).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_rowconfigure(4, weight=1) # Allow search frame to expand vertically

        # --- Contact List (Treeview) ---
        contact_list_frame = ttk.Frame(main_frame, padding="10 10 10 10")
        contact_list_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Define columns for the Treeview
        columns = ('name', 'phone', 'email', 'address')
        self.contact_tree = ttk.Treeview(contact_list_frame, columns=columns, show='headings', selectmode='browse')

        # Setup headings
        self.contact_tree.heading('name', text='Name', anchor=tk.W)
        self.contact_tree.heading('phone', text='Phone', anchor=tk.W)
        self.contact_tree.heading('email', text='Email', anchor=tk.W)
        self.contact_tree.heading('address', text='Address', anchor=tk.W)

        # Setup column widths
        self.contact_tree.column('name', width=150, minwidth=100)
        self.contact_tree.column('phone', width=120, minwidth=80)
        self.contact_tree.column('email', width=180, minwidth=120)
        self.contact_tree.column('address', width=200, minwidth=150)

        self.contact_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(contact_list_frame, orient="vertical", command=self.contact_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contact_tree.configure(yscrollcommand=scrollbar.set)

        # Bind selection event to populate fields
        self.contact_tree.bind('<<TreeviewSelect>>', self.on_contact_select)

        # --- Delete Button ---
        delete_button_frame = ttk.Frame(main_frame, padding="5 0 5 0")
        delete_button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        ttk.Button(delete_button_frame, text="Delete Selected Contact", command=self.delete_contact).pack(side=tk.RIGHT, padx=5, pady=5)


        # Configure row and column weights for main_frame
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1) # Contact list takes most vertical space

    def get_input_data(self):
      
        return {
            'name': self.entries['name'].get().strip(),
            'phone': self.entries['phone'].get().strip(),
            'email': self.entries['email'].get().strip(),
            'address': self.entries['address'].get().strip(),
        }

    def clear_fields(self):
        
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def populate_fields(self, contact):
        
        self.clear_fields()
        self.entries['name'].insert(0, contact.get('name', ''))
        self.entries['phone'].insert(0, contact.get('phone', ''))
        self.entries['email'].insert(0, contact.get('email', ''))
        self.entries['address'].insert(0, contact.get('address', ''))

    def add_contact(self):
        
        data = self.get_input_data()
        # Only 'name' and 'phone' are mandatory
        if not data['name'] or not data['phone']:
            messagebox.showwarning("Input Error", "Name and Phone are required fields.")
            return

        if self.app_controller.add_contact(data):
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_fields()
            self.refresh_contact_list()
        else:
            messagebox.showerror("Error", "Failed to add contact. Phone number might already exist.")

    def update_contact(self):
       
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a contact to update.")
            return

        # Get the old phone number from the selected item
        old_phone = self.contact_tree.item(selected_item, 'values')[1] # Phone is the second column

        data = self.get_input_data()
        # Only 'name' and 'phone' are mandatory for update
        if not data['name'] or not data['phone']:
            messagebox.showwarning("Input Error", "Name and Phone are required fields for update.")
            return

        if self.app_controller.update_contact(old_phone, data):
            messagebox.showinfo("Success", "Contact updated successfully!")
            self.clear_fields()
            self.refresh_contact_list()
        else:
            messagebox.showerror("Error", f"Failed to update contact with phone {old_phone}.")

    def delete_contact(self):
        
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")
            return

        # Get the phone number from the selected item
        phone_to_delete = self.contact_tree.item(selected_item, 'values')[1] # Phone is the second column

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete contact with phone: {phone_to_delete}?"):
            if self.app_controller.delete_contact(phone_to_delete, by_phone=True):
                messagebox.showinfo("Success", "Contact deleted successfully!")
                self.clear_fields()
                self.refresh_contact_list()
            else:
                messagebox.showerror("Error", "Failed to delete contact.")

    def search_contacts(self):
       
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query.")
            return

        by_phone = (self.search_by_var.get() == "phone")
        results = self.app_controller.search_contacts(query, by_phone=by_phone)
        self.display_contacts(results)
        if not results:
            messagebox.showinfo("No Results", "No contacts found matching your query.")

    def refresh_contact_list(self):
        
        all_contacts = self.app_controller.get_all_contacts()
        self.display_contacts(all_contacts)

    def display_contacts(self, contacts):
      
        # Clear existing items in the treeview
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)

        # Insert new contacts
        for contact in contacts:
            self.contact_tree.insert('', tk.END, values=(
                contact.get('name', ''),
                contact.get('phone', ''),
                contact.get('email', ''),
                contact.get('address', '')
            ))

    def on_contact_select(self, event):
        """
        Event handler for when a contact is selected in the Treeview.
        Populates the input fields with the selected contact's details.
        """
        selected_item = self.contact_tree.selection()
        if selected_item:
            values = self.contact_tree.item(selected_item, 'values')
            # Create a dictionary from the values to pass to populate_fields
            contact = {
                'name': values[0],
                'phone': values[1],
                'email': values[2],
                'address': values[3],
            }
            self.populate_fields(contact)

