# Contacts

An address book implemented in Python

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
./.venv/bin/Activate.ps1
```

Fetch the dependencies (except for tkinter) 
```shell
pip install -r requirements.txt
```

## Run

```shell
python -m contacts.main
```

## Build fat executable

Package application and dependencies as a single executable file

```shell
pyinstaller --windowed --onefile contacts/main.py
```
