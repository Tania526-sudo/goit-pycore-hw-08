from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.strptime(value, "%Y-%m-%d").date()

class Record:
    def __init__(self, name: Name):
        self.name = name
        self.phones = []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def __str__(self):
        return f"{self.name.value}: {', '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
