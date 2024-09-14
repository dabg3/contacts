from typing import Sequence
from contacts.core import Person

fields_mapping = {
        "name": 0,
        "surname": 1,
        "address": 2,
        "telephone": 3,
        "age": 4,
}


def retrieve_all() -> Sequence[Person]:
    contacts = []
    with open("informazioni.txt", "r") as file:
        for line in file:
            # strip trailing '\n'
            fields = line[:-1].split(";")
            p = Person(fields[0], fields[1], fields[2], fields[3], fields[4])
            contacts.append(p)
    return contacts


def insert(p: Person) -> None:
    return


def delete(p: Person) -> None:
    return
