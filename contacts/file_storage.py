from typing import Sequence
from contacts.core import Person

_config = None


def _assert_dependencies() -> None:
    if not _config:
        raise ValueError(
                f"invalid config dependency in {__name__}. Did you init()?"
                )


def init(config_module) -> None:
    global _config
    _config = config_module
    _assert_dependencies()


def _as_string(p: Person) -> str:
    age = p.age if p.age else ""
    return f"{p.name};{p.surname};{p.address};{p.telephone};{age}\n"


def retrieve_all() -> Sequence[Person]:
    _assert_dependencies()
    contacts = []
    with open(_config.get_storage_path(), "r") as file:
        for line in file:
            # strip trailing '\n'
            fields = line[:-1].split(";")
            p = Person(fields[0], fields[1], fields[2], fields[3], fields[4])
            contacts.append(p)
    return contacts


def insert(p: Person) -> None:
    _assert_dependencies()
    with open(_config.get_storage_path(), "a") as file:
        file.write(_as_string(p))


def update(old: Person, new: Person) -> None:
    _assert_dependencies()
    with open(_config.get_storage_path(), "r+") as file:
        lines = file.readlines()
        file.seek(0)
        i = lines.index(_as_string(old))
        lines[i] = _as_string(new)
        file.truncate()
        file.writelines(lines)


def delete(p: Person) -> None:
    _assert_dependencies()
    with open(_config.get_storage_path(), "r+") as file:
        lines = file.readlines()
        file.seek(0)
        i = lines.index(_as_string(p))
        lines.pop(i)
        file.truncate()
        file.writelines(lines)
