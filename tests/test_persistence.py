from pathlib import Path
from src.address_book import AddressBook, Record
from src.storage import save_data, load_data

def test_pickle_roundtrip(tmp_path: Path):
    pkl = tmp_path / "book.pkl"

    # Створили і зберегли
    book = AddressBook()
    r = Record("Alice")
    r.add_phone("0123456789")
    r.add_birthday("01.01.1990")
    book.add_record(r)
    save_data(book, pkl)

    # Завантажили і перевірили
    restored = load_data(pkl)
    a = restored.find("Alice")
    assert a is not None
    assert {p.value for p in a.phones} == {"0123456789"}
    assert a.birthday and a.birthday.value == "01.01.1990"