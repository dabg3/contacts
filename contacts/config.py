import os
import configparser

# warning: posix represents OSX also. If not posix, it is assumed to be windows
# https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on/
_os_config_dir = os.path.expanduser("~/.config/") \
        if os.name == "posix" \
        else os.getenv("LOCALAPPDATA") + "/"
_app_config_dir = _os_config_dir + "contacts/"
_config_file = _app_config_dir + "config.properties"

_config = None


def parse() -> None:
    global _config
    _assert_or_create_files()
    _config = configparser.ConfigParser()
    _config.read(_config_file)


def _assert_or_create_files() -> None:
    if not os.path.isdir(_app_config_dir):
        os.mkdir(_app_config_dir)
    if os.path.isfile(_config_file):
        return
    # write defaults
    config = configparser.ConfigParser()
    config["DEFAULT"]["file_storage_path"] = "info.txt"
    config["persistence"] = {}
    with open(_config_file, "w") as file:
        config.write(file)


def get_storage_path() -> str:
    return _config.get("persistence", "file_storage_path")


def set_storage_path(p: str) -> None:
    global _storage_path
    if not p or not os.path.isfile(p):
        return
    _config["persistence"]["file_storage_path"] = p
    with open(_config_file) as file:
        _config.write(file)
