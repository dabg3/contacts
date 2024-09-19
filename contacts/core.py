from typing import Sequence, Callable, Any


class Person(object):

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
        # DON'T allow assignments after instantiation,
        # enforce updates via update_contact(old, new)
        if hasattr(self, "_initialized"):
            return
        object.__setattr__(self, name, value)


_persistence = None
_contacts: list[Person] = []


# persistence modules MUST expose the same interface:
#   - retrieve_all()
#   - insert(person)
#   - update(old, new)
#   - delete(person)
def init(persistence_module=None) -> None:
    global _persistence
    if not persistence_module:
        return
    _persistence = persistence_module
    refresh_data()


def refresh_data() -> None:
    _contacts.clear()
    if not _persistence:
        return
    for p in _persistence.retrieve_all():
        _contacts.append(p)


def add_contact(p: Person) -> None:
    if p in _contacts:
        return
    for c in _contacts:
        if c.telephone == p.telephone:
            return
    if _persistence:
        _persistence.insert(p)
    _contacts.append(p)


def update_contact(old: Person, new: Person) -> None:
    if _persistence:
        _persistence.update(old, new)
    i = _contacts.index(old)
    _contacts[i] = new


def delete_contact(p: Person) -> None:
    if p not in _contacts:
        return
    if _persistence:
        _persistence.delete(p)
    _contacts.remove(p)


def get_all_contacts(sort_field_supplier: Callable[[Person], Any] = None,
                     reverse: bool = False) -> Sequence[Person]:
    # paging options can be implemented here in case of too many contacts
    list = _contacts.copy()
    return sorted(list, key=sort_field_supplier, reverse=reverse) \
        if sort_field_supplier else list
