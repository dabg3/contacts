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


# TODO: use element.update() instead of closing and recreating the window


def init_main_window(contacts: Sequence[Person]) -> None:
    global _main_window
    global _main_layout
    table_entries = list(map(convert_model, contacts))
    _main_layout = [[sg.Table(table_entries,
                              headings=["name", "surname", "telephone"],
                              select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                              enable_events=True)],
                    [sg.Button('New'),
                     sg.Button('Edit'),
                     sg.Button('Remove')]]
    _main_window = sg.Window('Contacts',
                             _main_layout,
                             finalize=True)


def update_contacts_table(contacts: Sequence[Person]) -> None:
    table_entries = list(map(convert_model, contacts))
    _main_layout[0][0].update(table_entries)


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
    _editor_layout = [[sg.Text("Name", size=10),
                       sg.Input(default_text=values[0], key='-NAME-')],
                      [sg.Text("Surname", size=10),
                       sg.Input(default_text=values[1], key='-SURNAME-')],
                      [sg.Text("Telephone", size=10),
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


def get_selected_contact() -> Person:
    selected_indexes = _main_layout[0][0].get()
    # ignore multiple selection
    return api.get_contact(selected_indexes[0]) if selected_indexes else None


_inserting_new = False


def handle_main_window_events(event, values) -> None:
    global _inserting_new
    match event:
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
            if _inserting_new:
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
                api.update_contact(get_selected_contact(), updated)
            _editor_window.close()
            update_contacts_table(api.get_all_contacts())
            _main_window.un_hide()


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
