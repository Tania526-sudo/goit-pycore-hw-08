# src/storage.py
from __future__ import annotations
import pickle
from pathlib import Path
from typing import Union, IO
from .address_book import AddressBook

DEFAULT_PATH = Path("addressbook.pkl")

def save_data(book: AddressBook, filename: Union[str, Path, IO[bytes]] = DEFAULT_PATH) -> None:
    if isinstance(filename, (str, Path)):
        with Path(filename).open("wb") as f:
            pickle.dump(book, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        pickle.dump(book, filename, protocol=pickle.HIGHEST_PROTOCOL)

def load_data(filename: Union[str, Path, IO[bytes]] = DEFAULT_PATH) -> AddressBook:
    try:
        if isinstance(filename, (str, Path)):
            with Path(filename).open("rb") as f:
                data = pickle.load(f)
        else:
            data = pickle.load(filename)
        return data if isinstance(data, AddressBook) else AddressBook()
    except FileNotFoundError:
        return AddressBook()
    except Exception:
        return AddressBook()
