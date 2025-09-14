# io_utils.py
import os, pickle
from .models import AddressBook

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "addressbook.pkl"))

def save_data(book, filename=DATA_PATH):
    os.makedirs(os.path.dirname(filename), exist_ok=True)   # <—
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=DATA_PATH):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.UnpicklingError):
        
        return AddressBook()

