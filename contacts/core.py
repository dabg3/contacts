class Person():

    def __init__(self,
                 name: str,
                 surname: str,
                 address: str,
                 telephone: str,
                 age: int):
        self.name = name
        self.surname = surname
        self.address = address
        self.telephone = telephone
        self.age = age


_contacts: set[Person] = []


def addContact(p: Person) -> None:
    # same instance
    if p in _contacts:
        return
    # duplicate number
    for c in _contacts:
        if c.telephone == p.telephone:
            return
    _contacts.add(p)


def removeContact(p: Person) -> None:
    if p not in _contacts:
        return
    _contacts.remove(p)
