from typing import Sequence
import PySimpleGUI as sg
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

_main_window = None
_editor_window = None
_contacts_view = None


def _update_contacts_table() -> None:
    global _contacts_view
    _contacts_view = _api.get_all_contacts(_sort_field_supplier,
                                           _reverse_ordering)
    table_entries = list(map(_convert_model, _contacts_view))
    _main_window.find_element("table").update(table_entries)


def _convert_model(p: Person) -> Sequence[str]:
    return [p.name, p.surname, p.telephone]


def _init_main_window() -> None:
    global _main_window
    menu_def = [["File", ["Settings"]]]
    main_layout = [[sg.Menu(menu_def)],
                   [sg.Table([],
                             headings=["Name", "Surname", "Telephone"],
                             key="table",
                             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                             auto_size_columns=False,
                             cols_justification=["l", "l", "l"],
                             col_widths=[15, 15, 15],
                             enable_events=True,
                             enable_click_events=True)],
                   [sg.Button('New'),
                    sg.Button('Edit'),
                    sg.Button('Remove')]]
    _main_window = sg.Window('Contacts',
                             main_layout,
                             finalize=True)
    _update_contacts_table()


def _init_editor_window(contact: Person = None) -> None:
    global _editor_window
    values = (contact.name,
              contact.surname,
              contact.telephone,
              contact.address,
              contact.age) if contact else ("", "", "", "", "")
    editor_layout = [[sg.Text("Name*", size=10),
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
                               editor_layout,
                               keep_on_top=True,
                               finalize=True)


def _get_selected_contact() -> Person:
    selected_indexes = _main_window.find_element("table").get()
    # ignore multiple selection
    return _contacts_view[selected_indexes[0]] if selected_indexes else None


_inserting_new = False


def _handle_main_window_events(event, values) -> None:
    global _inserting_new
    if isinstance(event, tuple) and event[0] == "table":
        _handle_sorting(event)
        return
    match event:
        case "Settings":
            filepath = sg.popup_get_file("Enter path to your data file:",
                                         multiple_files=False,
                                         no_titlebar=True)
            _config.set_storage_path(filepath)
            _api.refresh_data()
            _update_contacts_table()
        case "New":
            _inserting_new = True
            _main_window.hide()
            _init_editor_window()
        case "Edit":
            if not _get_selected_contact():
                _show_not_selected_popup()
                return
            _inserting_new = False
            _main_window.hide()
            _init_editor_window(_get_selected_contact())
        case "Remove":
            if not _get_selected_contact():
                _show_not_selected_popup()
                return
            confirm = sg.popup_yes_no(
                    "Do you really want to delete the contact?",
                    no_titlebar=True
                    )
            if confirm == "Yes":
                _api.delete_contact(_get_selected_contact())
                _update_contacts_table()


_reverse_ordering = False
_sort_field_supplier = None


def _handle_sorting(event) -> None:
    global _sort_field_supplier
    global _reverse_ordering
    # assert header was clicked and wasn't the "row" column
    if event[2][0] != -1 or event[2][1] == -1:
        return
    col_num_clicked = event[2][1]
    match col_num_clicked:
        case 0:
            _reverse_ordering = _supply_name == _sort_field_supplier \
                    and not _reverse_ordering
            _sort_field_supplier = _supply_name
        case 1:
            _reverse_ordering = _supply_surname == _sort_field_supplier \
                    and not _reverse_ordering
            _sort_field_supplier = _supply_surname
        case 2:
            _reverse_ordering = _supply_telephone == _sort_field_supplier \
                    and not _reverse_ordering
            _sort_field_supplier = _supply_telephone
    _update_contacts_table()


def _show_not_selected_popup() -> None:
    _main_window.hide()
    sg.popup("Select a contact from the table", no_titlebar=True)
    _main_window.un_hide()


def _handle_editor_window_events(event, values) -> None:
    global _inserting_new
    match event:
        case "Cancel" | sg.WIN_CLOSED:
            _editor_window.close()
            _main_window.un_hide()
        case "Save":
            if not _is_valid_input(values):
                return
            p = _instance_person(values)
            if _inserting_new:
                _api.add_contact(p)
            else:
                _api.update_contact(_get_selected_contact(), p)
            _editor_window.close()
            _update_contacts_table()
            _main_window.un_hide()


def _is_valid_input(values) -> bool:
    if not values["-NAME-"].strip():
        return False
    if not values["-SURNAME-"].strip():
        return False
    if not values["-TELEPHONE-"].strip():
        return False
    age = values["-AGE-"].strip()
    if not age:
        return True
    try:
        int(age)
    except ValueError:
        return False
    return True


def _instance_person(values) -> Person:
    age = int(values["-AGE-"]) if values["-AGE-"].strip() else None
    p = Person(values["-NAME-"].strip(),
               values["-SURNAME-"].strip(),
               values["-ADDRESS-"].strip(),
               values["-TELEPHONE-"].strip(),
               age)
    return p


def start() -> None:
    global _sort_field_supplier
    _assert_dependencies()
    # sort contacts by name
    _sort_field_supplier = _supply_name
    _init_main_window()
    while True:
        window, event, values = sg.read_all_windows()
        if window == _main_window:
            if event == sg.WIN_CLOSED:
                break
            _handle_main_window_events(event, values)
        else:
            _handle_editor_window_events(event, values)
    _main_window.close()


def _supply_name(p: Person) -> str:
    return p.name.lower()


def _supply_surname(p: Person) -> str:
    return p.surname.lower()


def _supply_telephone(p: Person) -> str:
    return p.telephone
