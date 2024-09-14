from typing import Sequence
import PySimpleGUI as sg
import contacts.core as api
from contacts.core import Person

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
                              headings=["name", "surname", "telephone"],
                              enable_events=True)],
                    [sg.Button('New'),
                     sg.Button('Edit'),
                     sg.Button('Remove')]]
    _main_window = sg.Window('Contacts',
                             _main_layout,
                             finalize=True)


def convert_model(p: Person) -> Sequence[str]:
    return [p.name, p.surname, p.telephone]


def init_editor_window(contact: tuple[str, str, str, str, str] = None) -> None:
    global _editor_window
    global _editor_layout
    if not contact or len(contact) != 5:
        contact = ("", "", "", "", "")
    _editor_layout = [[sg.Text("Name", size=10),
                       sg.Input(default_text=contact[0], key='-NAME-')],
                      [sg.Text("Surname", size=10),
                       sg.Input(default_text=contact[1], key='-SURNAME-')],
                      [sg.Text("Telephone", size=10),
                       sg.Input(default_text=contact[2], key='-TELEPHONE-')],
                      [sg.Text("Address", size=10),
                       sg.Input(default_text=contact[3], key='-ADDRESS-')],
                      [sg.Text("Age", size=10),
                       sg.Input(default_text=contact[4], key='-AGE-')],
                      [sg.Button('Save'),
                       sg.Button('Cancel')]]
    _editor_window = sg.Window('Editor',
                               _editor_layout,
                               keep_on_top=True,
                               finalize=True)


_selected_contact = None


def handle_main_window_events(event, values) -> None:
    global _selected_contact
    match event:
        case 0:
            _selected_contact = api.get_contact(values[0][0])
        case "New":
            _selected_contact = None
            _main_window.close()
            init_editor_window()
        case "Edit":
            if not _selected_contact:
                return
            _main_window.close()
            init_editor_window((_selected_contact.name,
                                _selected_contact.surname,
                                _selected_contact.telephone,
                                _selected_contact.address,
                                _selected_contact.age))


def handle_editor_window_events(event, values) -> None:
    match event:
        case "Cancel":
            _editor_window.close()
            init_main_window(api.get_all_contacts())
        case "Save":
            if not _selected_contact:
                new = Person(values["-NAME-"],
                             values["-SURNAME-"],
                             values["-ADDRESS-"],
                             values["-TELEPHONE-"],
                             values["-AGE-"])
                api.add_contact(new)
            else:
                updated = Person(values["-NAME-"],
                                 values["-SURNAME-"],
                                 values["-ADDRESS-"],
                                 values["-TELEPHONE-"],
                                 values["-AGE-"])
                api.update_contact(_selected_contact, updated)
            _editor_window.close()
            init_main_window(api.get_all_contacts())


if __name__ == "__main__":
    import contacts.file_storage as persistence
    api.init_app_state(persistence)
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
