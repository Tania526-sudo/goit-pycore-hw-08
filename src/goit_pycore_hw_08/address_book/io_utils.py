import pickle
import os
from .models import AddressBook

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "addressbook.pkl")

def save_data(book, filename=DATA_PATH):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename=DATA_PATH):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  
