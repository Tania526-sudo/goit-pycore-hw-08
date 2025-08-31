from .models import AddressBook, Record, Name, Phone, Birthday
from .io_utils import save_data, load_data

def main():
    book = load_data()

    while True:
        command = input("Введіть команду (add/show/exit): ")

        if command == "add":
            name = input("Ім'я: ")
            phone = input("Телефон: ")
            record = Record(Name(name))
            record.add_phone(Phone(phone))
            book.add_record(record)

        elif command == "show":
            for name, record in book.data.items():
                print(record)

        elif command == "exit":
            save_data(book)
            print("Дані збережено. До побачення!")
            break

        else:
            print("Невідома команда.")