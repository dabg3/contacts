from typing import Sequence
from contacts.core import Person


_filename = "info.txt"


def _as_string(p: Person):
    age = p.age if p.age else ""
    return f"{p.name};{p.surname};{p.address};{p.telephone};{age}\n"


def retrieve_all() -> Sequence[Person]:
    contacts = []
    with open(_filename, "r") as file:
        for line in file:
            # strip trailing '\n' or ';' in case age is not evaluated
            fields = line[:-1].split(";")
            p = Person(fields[0], fields[1], fields[2], fields[3], fields[4])
            contacts.append(p)
    return contacts


def insert(p: Person) -> None:
    with open(_filename, "a") as file:
        file.write(_as_string(p))


def update(old: Person, new: Person) -> None:
    with open(_filename, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        i = lines.index(_as_string(old))
        lines[i] = _as_string(new)
        file.truncate()
        file.writelines(lines)


def delete(p: Person) -> None:
    with open(_filename, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        i = lines.index(_as_string(p))
        lines.pop(i)
        file.truncate()
        file.writelines(lines)
