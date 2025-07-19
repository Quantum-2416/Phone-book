import json
import os

# Define the file path for storing contacts
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """
    Loads contacts from the JSON file.
    If the file does not exist, it returns an empty list.
    """
    if not os.path.exists(CONTACTS_FILE):
        return []
    try:
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Handle case where JSON file is empty or corrupted
        return []

def save_contacts(contacts):
    """
    Saves the current list of contacts to the JSON file.
    """
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

def add_contact(contact):
    """
    Adds a new contact to the list and saves it.
    Args:
        contact (dict): A dictionary containing contact details
                        (e.g., {'name': 'John Doe', 'phone': '123-456-7890', ...}).
    Returns:
        bool: True if contact was added successfully, False otherwise (e.g., duplicate phone).
    """
    contacts = load_contacts()
    # Check for duplicate phone number
    if any(c['phone'] == contact['phone'] for c in contacts):
        print(f"Error: Contact with phone number {contact['phone']} already exists.")
        return False
    contacts.append(contact)
    save_contacts(contacts)
    return True

def delete_contact(identifier, by_phone=True):
    """
    Deletes a contact by phone number or name.
    Args:
        identifier (str): The phone number or name to identify the contact.
        by_phone (bool): If True, search by phone number; otherwise, search by name.
    Returns:
        bool: True if contact was deleted, False otherwise.
    """
    contacts = load_contacts()
    initial_len = len(contacts)
    if by_phone:
        contacts = [c for c in contacts if c['phone'] != identifier]
    else:
        contacts = [c for c in contacts if c['name'].lower() != identifier.lower()]

    if len(contacts) < initial_len:
        save_contacts(contacts)
        return True
    return False

def search_contacts(query, by_phone=True):
    """
    Searches for contacts by phone number or name.
    Args:
        query (str): The search query.
        by_phone (bool): If True, search by phone number; otherwise, search by name.
    Returns:
        list: A list of matching contact dictionaries.
    """
    contacts = load_contacts()
    results = []
    query_lower = query.lower()
    for contact in contacts:
        if by_phone:
            if query_lower in contact['phone'].lower():
                results.append(contact)
        else:
            if query_lower in contact['name'].lower():
                results.append(contact)
    return results

def update_contact(old_phone, new_contact_data):
    """
    Updates an existing contact identified by their old phone number.
    Args:
        old_phone (str): The phone number of the contact to update.
        new_contact_data (dict): A dictionary with the new contact details.
                                 Keys can include 'name', 'phone', 'email', 'address'.
    Returns:
        bool: True if contact was updated, False otherwise.
    """
    contacts = load_contacts()
    found = False
    for i, contact in enumerate(contacts):
        if contact['phone'] == old_phone:
            # Update only the provided fields
            for key, value in new_contact_data.items():
                contacts[i][key] = value
            found = True
            break
    if found:
        save_contacts(contacts)
    return found

if __name__ == '__main__':
    # Example usage of the storage functions
    print("--- Storage Module Test ---")

    # Clear contacts for a clean test
    save_contacts([])

    # Add contacts
    add_contact({'name': 'Alice Smith', 'phone': '111-222-3333', 'email': 'alice@example.com', 'address': '123 Main St'})
    add_contact({'name': 'Bob Johnson', 'phone': '444-555-6666', 'email': 'bob@example.com', 'address': '456 Oak Ave'})
    add_contact({'name': 'Charlie Brown', 'phone': '777-888-9999', 'email': 'charlie@example.com', 'address': '789 Pine Ln'})

    print("\nAll contacts after adding:")
    print(load_contacts())

    # Search contacts
    print("\nSearching for 'Alice' by name:")
    print(search_contacts('Alice', by_phone=False))

    print("\nSearching for '444' by phone:")
    print(search_contacts('444', by_phone=True))

    # Update contact
    print("\nUpdating Alice's email:")
    update_contact('111-222-3333', {'email': 'alice.smith@newmail.com', 'address': 'New Alice Address'})
    print(load_contacts())

    # Delete contact
    print("\nDeleting Bob by phone:")
    delete_contact('444-555-6666', by_phone=True)
    print(load_contacts())

    print("\nDeleting Charlie by name:")
    delete_contact('Charlie Brown', by_phone=False)
    print(load_contacts())
