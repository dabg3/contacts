# Contacts

An address book implemented in Python

Features
* cross-platform
* configurable data file location `File > Settings`
* sorting by click on column headers

## Configuration
The configuration file `config.properties` is located in
`~/.config/contacts/` on POSIX systems, in 
`%localappdata%/contacts/` on Windows

It is managed by the application and should not be manually edited

## Dependencies

The application has been tested on Python 3.12, 
Python>=3.10 may work as well.

* PySimpleGui (it requires a license, select 30-day trial)
* python3-tkinter 
    - Windows: select 'tcl/tk' option while setting up Python
    - Linux: install via package manager

### Install dependencies on a virtual environment

Using venv is recommended to avoid polluting system packages

Initialize virtual enviroment
```shell
python -m venv venv
```

Activate on Linux 
```shell
source venv/bin/activate
```

Activate on Windows (PowerShell)
```shell
./venv/Scripts/Activate.ps1
```

Fetch the dependencies (except for tkinter) 
```shell
pip install -r requirements.txt
```

## Run

```shell
python -m contacts.contacts
```

## Build fat executable

Package application and dependencies as a single executable file

```shell
mkdir build && cd build
pyinstaller --windowed --onefile ../contacts/contacts.py
```

executable is located in `build/dist` folder
