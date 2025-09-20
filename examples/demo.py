# examples/demo.py
from src.address_book import AddressBook, Record

def demo():
    book = AddressBook()
    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("5555555555")
    john.add_birthday("01.01.1990")
    book.add_record(john)

    jane = Record("Jane")
    jane.add_phone("9876543210")
    jane.add_birthday("05.01.1995")
    book.add_record(jane)

    print(book)
    print("\nUpcoming birthdays (7 days):")
    for item in book.get_upcoming_birthdays():
        print(f"{item['birthday']}: {item['name']}")

if __name__ == "__main__":
    demo()
