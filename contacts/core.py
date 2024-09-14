from typing import Sequence


class Person(object):

    _initialized = False

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
        self._initialized = True

    def __setattr__(self, name, value):
        # DON'T allow assignments after instantiation
        if self._initialized:
            return
        object.__setattr__(self, name, value)


_persistence = None
_contacts: list[Person] = []


# dependency injection, persistence modules should implement the same interface
def init_app_state(persistence_module=None) -> None:
    global _persistence
    if not persistence_module:
        return
    _persistence = persistence_module
    for p in _persistence.retrieve_all():
        _contacts.append(p)


def add_contact(p: Person) -> None:
    # same instance
    if p in _contacts:
        return
    # duplicate number
    for c in _contacts:
        if c.telephone == p.telephone:
            return
    if _persistence:
        _persistence.insert(p)
    _contacts.append(p)


def update_contact(old: Person, new: Person):
    return


def delete_contact(p: Person) -> None:
    if p not in _contacts:
        return
    if _persistence:
        _persistence.delete(p)
    _contacts.remove(p)


def get_contact(index: int) -> Person:
    return _contacts[index]


def get_all_contacts() -> Sequence[Person]:
    return _contacts.copy()
