from typing import Sequence
import PySimpleGUI as sg
import contacts.core as api
from contacts.core import Person

_config = None
_api = None


def _assert_dependencies() -> None:
    if not _config:
        raise ValueError(
                f"invalid config dependency in {__name__}. Did you init()?"
                )
    if not _api:
        raise ValueError(
                f"invalid api dependency in {__name__}. Did you init()?"
                )


def init(config_module, api_module) -> None:
    global _config
    global _api
    _config = config_module
    _api = api_module
    _assert_dependencies()


sg.theme("gray gray gray")

# window and layout are set at runtime
# because elements (button, text, input) instances
# cannot be reused.
_main_layout = None
_main_window = None
_editor_layout = None
_editor_window = None


def init_main_window(contacts: Sequence[Person]) -> None:
    global _main_window
    global _main_layout
    table_entries = list(map(convert_model, contacts))
    _main_layout = [[sg.Table(table_entries,
                              headings=["Name", "Surname", "Telephone"],
                              select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                              auto_size_columns=False,
                              cols_justification=["l", "l", "l"],
                              col_widths=[15, 15, 15],
                              enable_events=True)],
                    [sg.Button('New'),
                     sg.Button('Edit'),
                     sg.Button('Remove')]]
    _main_window = sg.Window('Contacts',
                             _main_layout,
                             finalize=True)


def convert_model(p: Person) -> Sequence[str]:
    return [p.name, p.surname, p.telephone]


def init_editor_window(contact: Person = None) -> None:
    global _editor_window
    global _editor_layout
    values = (contact.name,
              contact.surname,
              contact.telephone,
              contact.address,
              contact.age) if contact else ("", "", "", "", "")
    _editor_layout = [[sg.Text("Name*", size=10),
                       sg.Input(default_text=values[0], key='-NAME-')],
                      [sg.Text("Surname*", size=10),
                       sg.Input(default_text=values[1], key='-SURNAME-')],
                      [sg.Text("Telephone*", size=10),
                       sg.Input(default_text=values[2], key='-TELEPHONE-')],
                      [sg.Text("Address", size=10),
                       sg.Input(default_text=values[3], key='-ADDRESS-')],
                      [sg.Text("Age", size=10),
                       sg.Input(default_text=values[4], key='-AGE-')],
                      [sg.Button('Save'),
                       sg.Button('Cancel')]]
    _editor_window = sg.Window('Editor',
                               _editor_layout,
                               keep_on_top=True,
                               finalize=True)


def update_contacts_table(contacts: Sequence[Person]) -> None:
    table_entries = list(map(convert_model, contacts))
    _main_layout[0][0].update(table_entries)


def get_selected_contact() -> Person:
    selected_indexes = _main_layout[0][0].get()
    # ignore multiple selection
    return api.get_contact(selected_indexes[0]) if selected_indexes else None


_inserting_new = False


def handle_main_window_events(event, values) -> None:
    global _inserting_new
    match event:
        case "Settings":
            filepath = sg.popup_get_file("Enter path to your .txt data file:")
            _config.set_storage_path(filepath)
        case "New":
            _inserting_new = True
            _main_window.hide()
            init_editor_window()
        case "Edit":
            if not get_selected_contact():
                return
            _inserting_new = False
            _main_window.hide()
            init_editor_window(get_selected_contact())
        case "Remove":
            if not get_selected_contact():
                return
            api.delete_contact(get_selected_contact())
            update_contacts_table(api.get_all_contacts())


def handle_editor_window_events(event, values) -> None:
    global _inserting_new
    match event:
        case "Cancel":
            _editor_window.close()
            _main_window.un_hide()
        case "Save":
            if not is_valid_input(values):
                return
            p = instance_person(values)
            if _inserting_new:
                api.add_contact(p)
            else:
                api.update_contact(get_selected_contact(), p)
            _editor_window.close()
            update_contacts_table(api.get_all_contacts())
            _main_window.un_hide()


def is_valid_input(values) -> bool:
    if not values["-NAME-"].strip():
        return False
    if not values["-SURNAME-"].strip():
        return False
    if not values["-TELEPHONE-"].strip():
        return False
    return True


def instance_person(values) -> Person:
    age = int(values["-AGE-"]) if values["-AGE-"].strip() else None
    p = Person(values["-NAME-"].strip(),
               values["-SURNAME-"].strip(),
               values["-ADDRESS-"].strip(),
               values["-TELEPHONE-"].strip(),
               age)
    return p


def start() -> None:
    _assert_dependencies()
    init_main_window(api.get_all_contacts())
    while True:
        window, event, values = sg.read_all_windows()
        if window == _main_window:
            if event == sg.WIN_CLOSED:
                break
            handle_main_window_events(event, values)
        else:
            handle_editor_window_events(event, values)
    _main_window.close()
