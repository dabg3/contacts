import PySimpleGUI as sg

_main_layout = [[sg.Table(["", "", ""],
                          headings=["name", "surname", "telephone"])],
                [sg.Button('New'),
                 sg.Button('Edit'),
                 sg.Button('Remove')]]

_main_window = sg.Window('Contacts',
                         _main_layout,
                         finalize=True)

# editor window and layout are set at runtime
# because elements (button, text, input) instances
# cannot be reused.
_editor_layout = None
_editor_window = None


def init_editor_window() -> sg.Window:
    global _editor_window
    global _editor_layout
    _editor_layout = [[sg.Text("Name", size=10),
                       sg.Input(key='-NAME-')],
                      [sg.Text("Surname", size=10),
                       sg.Input(key='-SURNAME-')],
                      [sg.Text("Telephone", size=10),
                       sg.Input(key='-TELEPHONE-')],
                      [sg.Text("Address", size=10),
                       sg.Input(key='-ADDRESS-')],
                      [sg.Text("Age", size=10),
                       sg.Input(key='-AGE-')],
                      [sg.Button('Save', size=10),
                       sg.Button('Cancel')]]
    _editor_window = sg.Window('Editor',
                               _editor_layout,
                               keep_on_top=True,
                               finalize=True)


def handle_main_window_events(event, values) -> None:
    if event == "New":
        init_editor_window()


def handle_editor_window_events(event, values) -> None:
    if event == "Cancel":
        _editor_window.close()
    elif event == "Save":
        # todo
        return


if __name__ == "__main__":
    while True:
        window, event, values = sg.read_all_windows()
        if window == _main_window:
            if event == sg.WIN_CLOSED:
                break
            handle_main_window_events(event, values)
        else:
            handle_editor_window_events(event, values)
    _main_window.close()
