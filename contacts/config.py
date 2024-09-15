import os

_storage_path = "info.txt"


def get_storage_path() -> str:
    return _storage_path


def set_storage_path(p: str) -> None:
    global _storage_path
    if not p or not os.path.isfile(p):
        return
    _storage_path = p
