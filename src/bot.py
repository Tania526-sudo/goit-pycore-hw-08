# src/bot.py
from functools import wraps
from typing import Callable, List, Tuple

from .address_book import AddressBook, Record
from .storage import load_data, save_data  

# --------- decorator ---------
def input_error(
    *,
    msg_value_error: str = "Give me correct data, please.",
    msg_key_error: str = "Contact not found.",
    msg_index_error: str = "Not enough arguments.",
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    def deco(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                return str(e) if str(e) else msg_value_error
            except KeyError:
                return msg_key_error
            except IndexError:
                return msg_index_error
        return wrapper
    return deco

# --------- helpers ---------
def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]

# --------- handlers ---------
@input_error(msg_value_error="Give me name and phone please.")
def add_contact(args: List[str], book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error(msg_value_error="Give me name, old phone and new phone please.")
def change_phone(args: List[str], book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error(msg_index_error="Enter user name.")
def show_phone(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    phones = ", ".join(p.value for p in record.phones) or "No phones."
    return phones

@input_error()
def show_all(args: List[str], book: AddressBook) -> str:
    return str(book)

@input_error(msg_value_error="Give me name and birthday in DD.MM.YYYY format.")
def add_birthday(args: List[str], book: AddressBook) -> str:
    name, bday, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(bday)
    return "Birthday added."

@input_error(msg_index_error="Enter user name.")
def show_birthday(args: List[str], book: AddressBook) -> str:
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError
    if record.birthday:
        return record.birthday.value
    return "Birthday is not set."

@input_error()
def birthdays(args: List[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays(days=7)
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = [f"{item['birthday']}: {item['name']}" for item in upcoming]
    return "\n".join(lines)

def main() -> None:
    # ЗАВАНТАЖЕННЯ 
    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ("close", "exit"):
            # ЗБЕРЕЖЕННЯ
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_phone(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "save":
            # Додатково
            save_data(book)
            print("Saved.")

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
