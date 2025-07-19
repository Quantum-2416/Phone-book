Python Contact Book Application
A simple, desktop-based Contact Book application built using Python's Tkinter for the GUI and JSON for local data storage. This application allows users to add, view, search, update, and delete contact information.

Features
Add Contacts: Easily add new contacts with their name, phone number, email, and address.

Mandatory Fields: Only Name and Phone Number are required for adding/updating contacts. Email and Address are optional.

View Contacts: Display all stored contacts in a clear, tabular format.

Search Contacts: Efficiently search for contacts by name or phone number.

Update Contacts: Modify existing contact details by selecting them from the list.

Delete Contacts: Remove unwanted contacts from the book.

Local Storage: All contact data is persisted locally in a contacts.json file.

User-Friendly GUI: Intuitive graphical interface built with Tkinter.

Screenshots/Demo
(You can add an animated GIF or a screenshot of your running application here. For example:)

(Replace the placeholder image URL above with a link to your actual GIF or image once you create it, as instructed previously.)

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
You need Python 3.x installed on your system.

Download Python

Installation
Clone the repository:

git clone https://github.com/Quantum-2416/Phone-book.git
cd Phone-book-repo

No external Python libraries are strictly required beyond the standard library (Tkinter and JSON are built-in). However, if you were to add more features requiring external libraries, you would typically install them like this:

# Example: If you needed a library like 'Pillow' for image handling
# pip install Pillow

Running the Application
Once you have cloned the repository and navigated into the project directory, you can run the application directly:

python contact_book_app.py

This will launch the Contact Book GUI.

Project Structure
The project is organized into three main Python files for clear separation of concerns:

contact_book_app.py: The main application entry point and controller. It initializes the GUI and acts as an intermediary between the UI and the data storage.

contact_book_ui.py: Contains all the Tkinter GUI elements, their layout, and handles user interaction events.

contact_book_storage.py: Manages all data persistence operations (loading, saving, adding, deleting, searching, updating contacts) to a contacts.json file.

How to Use
Add a Contact:

Fill in the "Name" and "Phone" fields (mandatory).

Optionally fill in "Email" and "Address".

Click the "Add Contact" button.

View All Contacts:

All contacts will be displayed in the table below the input fields.

Click "Show All" to refresh the list and display all contacts after a search.

Update a Contact:

Select a contact from the table by clicking on its row. The contact's details will populate the input fields.

Modify the desired fields.

Click the "Update Contact" button.

Search Contacts:

Enter a query in the "Search Query" field.

Select "By Phone" or "By Name" radio button.

Click the "Search" button. The table will update to show matching contacts.

Delete a Contact:

Select the contact you wish to delete from the table.

Click the "Delete Selected Contact" button.

Confirm the deletion in the pop-up window.

Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add new feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Built with Python and Tkinter.

Inspired by basic contact management needs.
