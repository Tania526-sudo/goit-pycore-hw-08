# main.py
from src.goit_pycore_hw_08.address_book.models import AddressBook, Record, Name, Phone, Birthday
from address_book.io_utils import save_data, load_data

def main():
    book = load_data()  

    while True:
        command = input(">>> ").strip().lower()

        if command == "add":
            name = input("Name: ")
            phone = input("Phone: ")
            record = Record(Name(name))
            record.add_phone(Phone(phone))
            book.add_record(record)

        elif command == "show all":
            for name, record in book.data.items():
                print(record)

        elif command == "exit":
            save_data(book)  
            print("До побачення!")
            break

        else:
            print("Невідома команда.")

if __name__ == "__main__":
    main()
