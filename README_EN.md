[![Custom Badge](https://img.shields.io/badge/-Back_to_spanish-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjRweCIgdmlld0JveD0iMCAtOTYwIDk2MCA5NjAiIHdpZHRoPSIyNHB4IiBmaWxsPSIjZTNlM2UzIj48cGF0aCBkPSJtNDc2LTgwIDE4Mi00ODBoODRMOTI0LTgwaC04NGwtNDMtMTIySDYwM0w1NjAtODBoLTg0Wk0xNjAtMjAwbC01Ni01NiAyMDItMjAycS0zNS0zNS02My41LTgwVDE5MC02NDBoODRxMjAgMzkgNDAgNjh0NDggNThxMzMtMzMgNjguNS05Mi41VDQ4NC03MjBINDB2LTgwaDI4MHYtODBoODB2ODBoMjgwdjgwSDU2NHEtMjEgNzItNjMgMTQ4dC04MyAxMTZsOTYgOTgtMzAgODItMTIyLTEyNS0yMDIgMjAxWm00NjgtNzJoMTQ0bC03Mi0yMDQtNzIgMjA0WiIvPjwvc3ZnPg==)](https://github.com/BeCuber/Turnomatic)

# Turnomatic
## *A desktop app to manage Volunteer availability*


## ![Index](./assets/images/title.png)
This repository contains the development of a desktop application designed to visualize and manage the availability dates provided by Volunteers for participation in an activity.

## Used Technologies
![Static Badge](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python)![Static Badge](https://img.shields.io/badge/SQLite-black?style=for-the-badge&logo=SQLite)![Static Badge](https://img.shields.io/badge/PyQt5-black?style=for-the-badge&logo=qt)

## Goals
The main goal is to provide the Coordinator with tools to visualize the availability of Volunteers, manage shift assignments, and ensure the minimum staffing required to deliver the service associated with the activities.

## Project Status
Development is currently in an **active building phase.**

### Architecture and Structure

The project follows a **modular and layered architector**, aiming for clean and maintainable code:

- `main.py`: runs the application
- `assets/`: contains external resources used in the code, currently just images
- `src/data`: holds the SQLite database and handles queries and data access
- `src/logic`: controller layer with specific logic for interacting with the database and exposing functions to the GUI
- `src/ui`: contains XML layout files created with [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html), and the code that builds the graphical interface. `main_window.py` is responsible for initializing and managing pages through a menu bar.
- `src/ui/pages`: defines each page of the application
- `src/ui/widgets`: custom widget classes used throughout the UI

 
This structure encourages code reuse and a clear separation of concerns between:
- **Model**: data access and management (`db_connector.py`)
- **View**: user interface defined with `.ui` files and [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html)
- **Controller**: interaction logic between data and GUI (`volunteer_manager.py`, `calendar_page.py`)

### Code Conventions

- Classes: `CamelCase`
- Functions and variables: `snake_case`
- Constants: `ALL_CAPS_WITH_UNDERSCORES`
- Files: `snake_case.py`
- Text visible in the application is in Spanish, while the source code is written in English

### Milestones
The following basic functionalities have already been implemented:

- Loading volunteer data from a local SQLite database
- Graphical interface with PyQt5 to visualize the data
- Separation of data logic from presentation
- Modular organization using widget managers (TextEdit, ComboBox, RadioButtons, etc.)
- Two pages are defined in the application, accessed through the menu bar
- `calendar_page.py`: Hosts a heatmap and allows editing of confirmed Volunteer groups from those available.
- `volunteer_page.py`: Displays the list of all Volunteers, a profile for each one, and the dates they are available.

### Next Steps

- Correctly implement the logic for enabling/disabling fields dependent on radio buttons (`volunteer_page.py`)
- Logic that handles date edits to keep records for consistent, user-readable periods
- Add field validation to forms
- Implement editing from all GUI fields (currently only retrieving data) (`volunteer_page.py`)
- Add database architecture to manage meal/dinner and bed needs
- Link date table data to calendars (`volunteer_page.py`)
- Design the heatmap (`calendar_page.py`)
- Internationalization
- Internal code documentation
- Packaging for cross-platform distribution (Windows/Linux)

## Notes
- **Personal use:** This code is primarily for learning and experimentation.
- **Not for Production Use:** This repository is not intended for deployment in production environments or other projects without prior review.

---
Thank you for visiting this website! I'm continuously learning, so any suggestions or feedback are always welcome.