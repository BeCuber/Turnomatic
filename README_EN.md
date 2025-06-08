[![Custom Badge](https://img.shields.io/badge/-Back_to_spanish-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGhlaWdodD0iMjRweCIgdmlld0JveD0iMCAtOTYwIDk2MCA5NjAiIHdpZHRoPSIyNHB4IiBmaWxsPSIjZTNlM2UzIj48cGF0aCBkPSJtNDc2LTgwIDE4Mi00ODBoODRMOTI0LTgwaC04NGwtNDMtMTIySDYwM0w1NjAtODBoLTg0Wk0xNjAtMjAwbC01Ni01NiAyMDItMjAycS0zNS0zNS02My41LTgwVDE5MC02NDBoODRxMjAgMzkgNDAgNjh0NDggNThxMzMtMzMgNjguNS05Mi41VDQ4NC03MjBINDB2LTgwaDI4MHYtODBoODB2ODBoMjgwdjgwSDU2NHEtMjEgNzItNjMgMTQ4dC04MyAxMTZsOTYgOTgtMzAgODItMTIyLTEyNS0yMDIgMjAxWm00NjgtNzJoMTQ0bC03Mi0yMDQtNzIgMjA0WiIvPjwvc3ZnPg==)](https://github.com/BeCuber/Turnomatic)

# Turnomatic
## *A desktop app to manage Volunteer availability*


## ![Index](./assets/images/title.png)
This repository contains the development of a desktop application designed to visualize and manage the availability dates provided by Volunteers for participation in an activity.

## Used Technologies
![Static Badge](https://img.shields.io/badge/Python-black?style=for-the-badge&logo=Python)![Static Badge](https://img.shields.io/badge/SQLite-black?style=for-the-badge&logo=SQLite)![Static Badge](https://img.shields.io/badge/PyQt5-black?style=for-the-badge&logo=qt)![Static Badge](https://img.shields.io/badge/ChatGPT-black?style=for-the-badge&logo=openai)

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

- Volunteer data loading from a local SQLite database.
- Graphical user interface (GUI) developed with PyQt5 for data visualization and editing.
- Clear separation between data logic and presentation layer.
- Organization of widget logic through specific managers (TextEdit, ComboBox, RadioButtons...).
- Two main pages defined in the application, accessible via the menu bar:
  - `calendar_page.py`: Includes a heatmap and allows editing of confirmed volunteer groups from the list of available ones.
  - `volunteer_page.py`: Displays a complete list of volunteers, their personal profiles, and their availability dates.
- Logic for toggling volunteer data editing mode fully implemented.
- Field validation to prevent data loss during editing.
- Management of coherent and user-friendly date ranges.
- GUI-based creation, editing, and deletion of volunteers and their availability (`volunteer_page.py`).
- Synchronization of calendars with per-volunteer date tables.
- Heatmap implementation in `calendar_page.py`.
- Packaged for distribution on Windows.
- UI is supported to various window sizes and screen resolutions.

### Next Steps

- Add a security layer for the database (evaluating SQLCipher).
- Extend the database structure to register meal and bed requirements.
- Add two new GUI pages to manage meals and beds.
- Implement internationalization (i18n) support.
- Add detailed internal documentation of the codebase.
- Package the application for cross-platform distribution (add Linux support).
- Create an installer to simplify software distribution and installation.

## Notes
- **Personal use:** This code is primarily for learning and experimentation.
- **Not for Production Use:** This repository is not intended for deployment in production environments or other projects without prior review.

---
Thank you for visiting this website! I'm continuously learning, so any suggestions or feedback are always welcome.