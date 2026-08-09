# Library Management System

A modular, object-oriented Library Management System built collaboratively in Python. Each module was developed independently by a dedicated group and then integrated into a single working application. A Tkinter-based GUI is also included as an alternative front end to the command-line interface.

## Project Overview

This project implements a simple library system that supports adding and searching books, registering members, issuing and returning books, and basic librarian authentication — available both as a command-line interface and as a desktop GUI.

## Modules

| Module | File | Responsibility |
|---|---|---|
| Group A | `book.py` | `Book` class: isbn, title, author, copies |
| Group B | `member.py` | `Member` class: member_id, name, borrowed_books |
| Group C | `library.py` | `Library` class: add/remove/list books |
| Group D | `issue_return.py` | Issue and return logic, updates availability |
| Group E | `search.py` | Search by title, author, or ISBN |
| Group F | `auth_system.py` | Basic username/password authentication |
| Group G | `library_management_system.py` | Main CLI application, ties all modules together |
| Group G (GUI) | `gui_app.py` | Tkinter desktop GUI, uses the same modules above |
| Group H | `test_library.py` | Unit tests for all modules |

## Folder Structure

```
library-management-system/
├── book.py
├── member.py
├── library.py
├── issue_return.py
├── search.py
├── auth_system.py
├── library_management_system.py
├── gui_app.py
├── test_library.py
├── README.md
└── .github/
    └── PULL_REQUEST_TEMPLATE.md
```

## Getting Started

### Requirements
- Python 3.8+
- `pytest` (for running unit tests)
- Tkinter (included with standard Python installs on Windows/Mac; on Linux install via `sudo apt install python3-tk`)

### Run the command-line application
```bash
python library_management_system.py
```

### Run the GUI application
```bash
python gui_app.py
```
On first run, log in with the seeded demo credentials:
- Username: `admin`
- Password: `admin123`

The GUI has five tabs: **Dashboard** (shown first, with a button for every function plus Logout/Exit), **Books** (add/view books), **Search** (by title, author, or ISBN), **Members** (add/view members), and **Issue / Return** (issue or return a book to a member). A **File** menu also offers Logout and Exit, and a **View** menu lets you toggle window resizing on/off.

### Run the tests
```bash
pip install pytest
pytest test_library.py -v
```

## Development Guidelines
- Use consistent variable names (`isbn`, `title`, `author`, `copies`, `member_id`, etc.).
- Follow agreed class/function names: `Book`, `Member`, `Library`, etc.
- Document each function and class with proper docstrings.
- Report interface changes to Group G immediately.
- Avoid changes after the first integration unless approved.

## GitHub Workflow

1. **Repository Setup** — Create the `library-management-system` repository with branch protection on `main`.
2. **Branch Naming** — Use `group-a-book`, `group-b-member`, etc., one branch per group/module.
3. **Development** — Code only on your assigned branch.
4. **Pull Requests** — Submit a PR to `main` when your module is complete. Use clear, descriptive PR titles and descriptions.
5. **Code Review** — Reviewers check code quality, naming conventions, and docstrings; request changes if necessary.
6. **Merge** — Merge only after successful review and passing tests.
7. **Testing** — Group H maintains `test_library.py` and verifies integrated functionality via unit tests, ideally run in CI on every PR.

## Contribution Guidelines
1. Fork/branch from `main` using your group's branch name.
2. Keep your changes scoped to your assigned module file.
3. Write or update docstrings for any new function/class.
4. Add or update unit tests in `test_library.py` where relevant.
5. Open a pull request using the template in `.github/PULL_REQUEST_TEMPLATE.md`.
6. Address review comments promptly and re-request review after changes.

## Final Deliverables
- Individual module files (`book.py`, `member.py`, `library.py`, `issue_return.py`, `search.py`, `auth_system.py`)
- Integrated CLI application file (`library_management_system.py`)
- GUI application file (`gui_app.py`)
- Testing file (`test_library.py`)
- Complete project documentation (`README.md`, PR template)
