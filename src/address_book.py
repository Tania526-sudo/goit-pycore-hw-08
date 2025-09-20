# src/address_book.py
import re
from collections import UserDict
from datetime import date, datetime, timedelta
from typing import List, Optional, Dict


# ---------- Base fields ----------

class Field:
    """Base class for all record fields."""

    def __init__(self, value: str):
        self._value: str = ""
        self.value = value  # validate via setter

    def __str__(self) -> str:
        return str(self.value)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        self._value = new_value


class Name(Field):
    """Required contact name."""

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str) -> None:
        if not isinstance(new_value, str):
            raise TypeError("Name must be a string.")
        new_value = new_value.strip()
        if not new_value:
            raise ValueError("Name cannot be empty.")
        self._value = new_value


class Phone(Field):
    """Phone number with validation: exactly 10 digits."""

    _rx = re.compile(r"^\d{10}$")

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str) -> None:
        if not isinstance(new_value, str):
            raise TypeError("Phone must be a string.")
        new_value = new_value.strip()
        if not self._rx.fullmatch(new_value):
            raise ValueError("Phone must contain exactly 10 digits.")
        self._value = new_value


class Birthday(Field):
    """
    Birthday with validation (DD.MM.YYYY).
    Stores the normalized string in `value`, provides `.as_date` helper.
    """

    @Field.value.setter  # type: ignore[misc]
    def value(self, new_value: str) -> None:
        if not isinstance(new_value, str):
            raise TypeError("Birthday must be a string in DD.MM.YYYY format.")
        new_value = new_value.strip()
        try:
            dt = datetime.strptime(new_value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        # store normalized (zero-padded) representation
        self._value = dt.strftime("%d.%m.%Y")

    @property
    def as_date(self) -> date:
        return datetime.strptime(self.value, "%d.%m.%Y").date()


# ---------- Record & AddressBook ----------

class Record:
    """Contact record: name (required), phones (0..N), optional birthday (0..1)."""

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    # phones
    def add_phone(self, phone: str) -> Phone:
        p = Phone(phone)
        self.phones.append(p)
        return p

    def remove_phone(self, phone: str) -> bool:
        for i, p in enumerate(self.phones):
            if p.value == phone:
                del self.phones[i]
                return True
        return False

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)  # validates
                return
        raise ValueError("Old phone not found.")

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # birthday
    def add_birthday(self, birthday_str: str) -> Birthday:
        """Add or overwrite birthday (validated)."""
        b = Birthday(birthday_str)
        self.birthday = b
        return b

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else ""
        bday_str = self.birthday.value if self.birthday else "—"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    """
    Storage for Records (dict-like).
    Keys: record.name.value, Values: Record
    """

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> bool:
        return self.data.pop(name, None) is not None

    def __str__(self) -> str:
        if not self.data:
            return "AddressBook is empty."
        lines = []
        for key in sorted(self.data.keys(), key=str.casefold):
            lines.append(str(self.data[key]))
        return "\n".join(lines)

    # --- birthdays within next `days` (default 7), including today ---
    def get_upcoming_birthdays(self, days: int = 7) -> List[Dict[str, str]]:
        """
        Returns a list of dicts: {"name": <Name>, "birthday": <DD.MM.YYYY of congratulation>}
        If birthday falls on Sat/Sun, congratulate on Monday.
        """
        result: List[Dict[str, str]] = []
        today = date.today()

        for rec in self.data.values():
            if not rec.birthday:
                continue

            bday = rec.birthday.as_date  # original year
            # make birthday date in current year (or next if already passed)
            this_year = date(today.year, bday.month, bday.day)
            if this_year < today:
                this_year = date(today.year + 1, bday.month, bday.day)

            delta = (this_year - today).days
            if 0 <= delta <= days:
                greet = this_year
                # shift to Monday if weekend (Sat=5, Sun=6)
                if greet.weekday() == 5:
                    greet += timedelta(days=2)
                elif greet.weekday() == 6:
                    greet += timedelta(days=1)

                result.append(
                    {"name": rec.name.value, "birthday": greet.strftime("%d.%m.%Y")}
                )

        # sort by congratulation date then name
        result.sort(key=lambda d: (datetime.strptime(d["birthday"], "%d.%m.%Y"), d["name"].casefold()))
        return result
