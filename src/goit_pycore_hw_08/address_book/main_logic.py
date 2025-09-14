from .models import AddressBook, Record, Name, Phone, Birthday
from .io_utils import save_data, load_data


def main():
    book = load_data()

    while True:
        command = input("Enter a command (add/show/exit): ")

        if command == "add":
            name = input("Name: ")
            phone = input("Phone: ")
            record = Record(Name(name))
            record.add_phone(Phone(phone))
            book.add_record(record)

        elif command == "show":
            for name, record in book.data.items():
                print(record)

        elif command == "exit":
            save_data(book)
            print("Data saved. Goodbye!")
            break

        else:
            print("Unknown command.")
