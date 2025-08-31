# Homework 8: Serializing AddressBook using pickle

This project demonstrates how to serialize an `AddressBook` object to persist contacts across sessions.

## Structure:
- `models.py`: Core classes for the address book.
- `io_utils.py`: Save/Load functions via pickle.
- `main.py`: Basic CLI logic for the user.

## How to use:
1. Run `main.py`
2. Type `add` to add a contact
3. Type `show all` to view
4. Type `exit` to save the data

The data is automatically saved to `addressbook.pkl` and will be restored on next run.