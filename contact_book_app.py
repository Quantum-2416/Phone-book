import tkinter as tk
from contact_book_storage import (
    load_contacts, save_contacts, add_contact,
    delete_contact, search_contacts, update_contact
)
from contact_book_ui import ContactBookUI

class ContactBookApp:
    def __init__(self):
        """
        Initializes the main Contact Book Application.
        Sets up the Tkinter root window and the UI.
        """
        self.root = tk.Tk()
        self.ui = ContactBookUI(self.root, self) # Pass self (the app controller) to the UI

    def add_contact(self, contact_data):
        """
        Adds a new contact using the storage module.
        Args:
            contact_data (dict): Dictionary containing contact details.
        Returns:
            bool: True if contact added, False otherwise.
        """
        return add_contact(contact_data)

    def delete_contact(self, identifier, by_phone=True):
        """
        Deletes a contact using the storage module.
        Args:
            identifier (str): Phone number or name of the contact.
            by_phone (bool): True to delete by phone, False by name.
        Returns:
            bool: True if contact deleted, False otherwise.
        """
        return delete_contact(identifier, by_phone)

    def search_contacts(self, query, by_phone=True):
        """
        Searches for contacts using the storage module.
        Args:
            query (str): Search string.
            by_phone (bool): True to search by phone, False by name.
        Returns:
            list: List of matching contact dictionaries.
        """
        return search_contacts(query, by_phone)

    def update_contact(self, old_phone, new_contact_data):
        """
        Updates an existing contact using the storage module.
        Args:
            old_phone (str): The phone number of the contact to update.
            new_contact_data (dict): Dictionary with updated contact details.
        Returns:
            bool: True if contact updated, False otherwise.
        """
        return update_contact(old_phone, new_contact_data)

    def get_all_contacts(self):
        """
        Retrieves all contacts from the storage module.
        Returns:
            list: List of all contact dictionaries.
        """
        return load_contacts()

    def run(self):
        """
        Starts the Tkinter event loop, making the GUI interactive.
        """
        self.root.mainloop()

if __name__ == '__main__':
    # When the app starts, ensure the contacts.json file is initialized if it doesn't exist
    # This prevents errors if the file is missing on first run
    try:
        load_contacts()
    except Exception:
        save_contacts([]) # Create an empty file if loading fails

    app = ContactBookApp()
    app.run()
