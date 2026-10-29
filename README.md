# Find My Book

## Overview
Library Book Finder is a Python application that helps users find library subjects, classmarks, and locations. It includes both a command-line interface (CLI) and a graphical user interface (GUI).

## Features
- Search for subjects using partial names.
- Find subjects using an exact classmark.
- Search for library locations.
- View matching results in the graphical interface.
- Use search history in the GUI.

## Technologies
- Python
- Tkinter
- CSV files

## Project Structure

```text
library-book-finder/
├── CLI.py
├── GUI.py
├── subjects.csv
├── locations.csv
├── README.md
└── .gitignore
```

## Getting Started

### Requirements
Install Python 3. The GUI uses Tkinter, which is included with many Python installations.

### Run the command-line interface

```bash
python CLI.py
```

### Run the graphical interface

```bash
python GUI.py
```

If your system uses the `python3` command, replace `python` with `python3`.

## Data Files
- `subjects.csv` contains subject names and their classmarks.
- `locations.csv` maps classmarks to library locations.

Keep both CSV files in the same directory as the Python scripts when running the application.

## Future Improvements
- Improve input validation and error handling.
- Add automated tests.
- Improve search and results presentation.

## Acknowledgements
Development assistance from AI tools should be acknowledged accurately in accordance with the relevant university guidance.
