"""
gui_app.py - Group G (GUI variant): Main Application Interface

Purpose: Provide a graphical (Tkinter) front end for the Library
Management System, using the same underlying modules as the CLI
version (book.py, member.py, library.py, issue_return.py, search.py,
auth_system.py). No changes to those modules are required.

Run with: python gui_app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from book import Book
from member import Member
from library import Library
from issue_return import issue_book, return_book
from search import search_by_title, search_by_author, search_by_isbn
from auth_system import authenticate


# ---------------------------------------------------------------------------
# Shared in-memory data (same idea as seed_demo_data() in the CLI version)
# ---------------------------------------------------------------------------

def seed_demo_data(library, members, user_db):
    """Populate the system with a few demo books, members, and a login."""
    library.add_book(Book("111", "Clean Code", "Robert C. Martin", 3))
    library.add_book(Book("222", "The Pragmatic Programmer", "David Thomas", 2))
    library.add_book(Book("333", "Introduction to Algorithms", "Thomas H. Cormen", 1))

    members["M001"] = Member("M001", "Alice Johnson")
    members["M002"] = Member("M002", "Bob Smith")

    user_db["admin"] = "admin123"


# ---------------------------------------------------------------------------
# Login window
# ---------------------------------------------------------------------------

class LoginWindow(tk.Tk):
    """First window shown: asks for username/password before the main app."""

    def __init__(self, library, members, user_db):
        super().__init__()
        self.library = library
        self.members = members
        self.user_db = user_db

        self.title("Library Management System - Login")
        self.geometry("360x220")
        self.resizable(True, True)   # allow the login window to be resized
        self.minsize(320, 200)       # don't let it shrink small enough to clip the form
        self.configure(padx=20, pady=20)

        ttk.Label(self, text="Library Management System", font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

        form = ttk.Frame(self)
        form.pack(fill="x")

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.username_var).grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(form, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5, sticky="ew")

        form.columnconfigure(1, weight=1)

        ttk.Label(self, text="Demo login: admin / admin123", foreground="gray").pack(pady=(10, 5))

        ttk.Button(self, text="Log In", command=self.try_login).pack(pady=10)

        # Let Enter key submit the form too
        self.bind("<Return>", lambda event: self.try_login())

    def try_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if authenticate(username, password, self.user_db):
            self.destroy()  # close the login window
            app = MainApp(self.library, self.members, self.user_db, username)
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")


# ---------------------------------------------------------------------------
# Main application window (shown after successful login)
# ---------------------------------------------------------------------------

class MainApp(tk.Tk):
    """Main window with a dashboard plus tabs for each library operation."""

    def __init__(self, library, members, user_db, logged_in_as):
        super().__init__()
        self.library = library
        self.members = members
        self.user_db = user_db
        self.logged_in_as = logged_in_as

        self.title(f"Library Management System - Logged in as {logged_in_as}")
        self.geometry("720x480")
        self.resizable(True, True)   # allow the main window to be resized
        self.minsize(600, 380)       # keep tabs/tables usable even at the smallest size

        # If the user closes the window with the X button, treat it the same
        # as choosing Exit (asks for confirmation instead of closing silently).
        self.protocol("WM_DELETE_WINDOW", self.exit_app)

        # --- Menu bar: File (Logout / Exit) and View (resizing toggle) ---
        self.resizable_var = tk.BooleanVar(value=True)
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_checkbutton(
            label="Allow Window Resizing",
            variable=self.resizable_var,
            command=self.toggle_resizable,
        )
        menubar.add_cascade(label="View", menu=view_menu)

        self.config(menu=menubar)

        # --- Tabs ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Build the functional tabs first, since the dashboard's buttons
        # need to be able to jump straight to them.
        self.books_tab = BooksTab(self.notebook, self.library)
        self.search_tab = SearchTab(self.notebook, self.library)
        self.members_tab = MembersTab(self.notebook, self.members)
        self.issue_return_tab = IssueReturnTab(self.notebook, self.library, self.members, self.books_tab)
        self.dashboard_tab = DashboardTab(self.notebook, self)

        # Dashboard is added first so it's the tab shown right after login.
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.books_tab, text="Books")
        self.notebook.add(self.search_tab, text="Search")
        self.notebook.add(self.members_tab, text="Members")
        self.notebook.add(self.issue_return_tab, text="Issue / Return")

        self.notebook.select(self.dashboard_tab)

    def go_to_tab(self, tab):
        """Switch the notebook to the given tab (used by the dashboard buttons)."""
        self.notebook.select(tab)

    def toggle_resizable(self):
        """Turn window resizing on or off based on the View menu checkbox."""
        allow = self.resizable_var.get()
        self.resizable(allow, allow)

    def logout(self):
        """Close the main window and return to the login screen.

        Library and member data is kept in memory and handed back to the
        new LoginWindow, so nothing is lost on logout - only re-authentication
        is required.
        """
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.destroy()
            login = LoginWindow(self.library, self.members, self.user_db)
            login.mainloop()

    def exit_app(self):
        """Close the main window and end the application entirely."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.destroy()


# ---------------------------------------------------------------------------
# Dashboard tab: shown right after login, one button per function
# ---------------------------------------------------------------------------

class DashboardTab(ttk.Frame):
    """Landing screen after login - a button for every major function."""

    def __init__(self, parent, main_app):
        super().__init__(parent, padding=20)
        self.main_app = main_app

        ttk.Label(
            self,
            text=f"Welcome, {main_app.logged_in_as}!",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(0, 5))
        ttk.Label(self, text="What would you like to do?").pack(pady=(0, 20))

        actions_frame = ttk.Frame(self)
        actions_frame.pack()

        # Each entry is (button label, which tab it should jump to)
        actions = [
            ("Add Book", main_app.books_tab),
            ("List Books", main_app.books_tab),
            ("Search Books", main_app.search_tab),
            ("Add Member", main_app.members_tab),
            ("View Members", main_app.members_tab),
            ("Issue / Return Book", main_app.issue_return_tab),
        ]

        for index, (label, target_tab) in enumerate(actions):
            row, col = divmod(index, 2)
            btn = ttk.Button(
                actions_frame,
                text=label,
                width=22,
                command=lambda tab=target_tab: main_app.go_to_tab(tab),
            )
            btn.grid(row=row, column=col, padx=10, pady=8, ipady=8)

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=20)

        session_frame = ttk.Frame(self)
        session_frame.pack()
        ttk.Button(session_frame, text="Logout", width=15, command=main_app.logout).pack(side="left", padx=10)
        ttk.Button(session_frame, text="Exit", width=15, command=main_app.exit_app).pack(side="left", padx=10)


# ---------------------------------------------------------------------------
# Books tab: add books, see the full list
# ---------------------------------------------------------------------------

class BooksTab(ttk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent, padding=10)
        self.library = library

        form = ttk.LabelFrame(self, text="Add a Book", padding=10)
        form.pack(fill="x", pady=(0, 10))

        self.isbn_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.copies_var = tk.StringVar()

        self._labeled_entry(form, "ISBN:", self.isbn_var, 0)
        self._labeled_entry(form, "Title:", self.title_var, 1)
        self._labeled_entry(form, "Author:", self.author_var, 2)
        self._labeled_entry(form, "Copies:", self.copies_var, 3)

        ttk.Button(form, text="Add Book", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)
        form.columnconfigure(1, weight=1)

        list_frame = ttk.LabelFrame(self, text="All Books", padding=10)
        list_frame.pack(fill="both", expand=True)

        columns = ("isbn", "title", "author", "copies")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col, label in zip(columns, ["ISBN", "Title", "Author", "Copies"]):
            self.tree.heading(col, text=label)
        self.tree.pack(fill="both", expand=True)

        self.refresh()

    def _labeled_entry(self, parent, label_text, var, row):
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew", pady=3)

    def add_book(self):
        isbn = self.isbn_var.get().strip()
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        copies_text = self.copies_var.get().strip()

        if not isbn or not title or not author:
            messagebox.showwarning("Missing Info", "ISBN, Title, and Author are required.")
            return
        try:
            copies = int(copies_text)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Copies must be a whole number.")
            return

        self.library.add_book(Book(isbn, title, author, copies))
        messagebox.showinfo("Success", f'Book "{title}" added.')

        # Clear the form
        self.isbn_var.set("")
        self.title_var.set("")
        self.author_var.set("")
        self.copies_var.set("")

        self.refresh()

    def refresh(self):
        """Reload the book list from the Library into the table."""
        self.tree.delete(*self.tree.get_children())
        for book in self.library.list_books():
            self.tree.insert("", "end", values=(book.isbn, book.title, book.author, book.copies))


# ---------------------------------------------------------------------------
# Search tab
# ---------------------------------------------------------------------------

class SearchTab(ttk.Frame):
    def __init__(self, parent, library):
        super().__init__(parent, padding=10)
        self.library = library

        controls = ttk.Frame(self)
        controls.pack(fill="x", pady=(0, 10))

        ttk.Label(controls, text="Search by:").pack(side="left")
        self.mode_var = tk.StringVar(value="title")
        ttk.Radiobutton(controls, text="Title", variable=self.mode_var, value="title").pack(side="left", padx=5)
        ttk.Radiobutton(controls, text="Author", variable=self.mode_var, value="author").pack(side="left", padx=5)
        ttk.Radiobutton(controls, text="ISBN", variable=self.mode_var, value="isbn").pack(side="left", padx=5)

        self.query_var = tk.StringVar()
        ttk.Entry(controls, textvariable=self.query_var).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(controls, text="Search", command=self.run_search).pack(side="left")

        columns = ("isbn", "title", "author", "copies")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col, label in zip(columns, ["ISBN", "Title", "Author", "Copies"]):
            self.tree.heading(col, text=label)
        self.tree.pack(fill="both", expand=True)

    def run_search(self):
        query = self.query_var.get().strip()
        mode = self.mode_var.get()

        if mode == "title":
            results = search_by_title(self.library, query)
        elif mode == "author":
            results = search_by_author(self.library, query)
        else:
            book = search_by_isbn(self.library, query)
            results = [book] if book else []

        self.tree.delete(*self.tree.get_children())
        for book in results:
            self.tree.insert("", "end", values=(book.isbn, book.title, book.author, book.copies))

        if not results:
            messagebox.showinfo("No Results", "No matching books found.")


# ---------------------------------------------------------------------------
# Members tab
# ---------------------------------------------------------------------------

class MembersTab(ttk.Frame):
    def __init__(self, parent, members):
        super().__init__(parent, padding=10)
        self.members = members

        form = ttk.LabelFrame(self, text="Add a Member", padding=10)
        form.pack(fill="x", pady=(0, 10))

        self.member_id_var = tk.StringVar()
        self.name_var = tk.StringVar()

        ttk.Label(form, text="Member ID:").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.member_id_var).grid(row=0, column=1, sticky="ew", pady=3)
        ttk.Label(form, text="Name:").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.name_var).grid(row=1, column=1, sticky="ew", pady=3)
        form.columnconfigure(1, weight=1)

        ttk.Button(form, text="Add Member", command=self.add_member).grid(row=2, column=0, columnspan=2, pady=10)

        list_frame = ttk.LabelFrame(self, text="All Members", padding=10)
        list_frame.pack(fill="both", expand=True)

        columns = ("member_id", "name", "borrowed")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col, label in zip(columns, ["Member ID", "Name", "Borrowed Books"]):
            self.tree.heading(col, text=label)
        self.tree.pack(fill="both", expand=True)

        self.refresh()

    def add_member(self):
        member_id = self.member_id_var.get().strip()
        name = self.name_var.get().strip()

        if not member_id or not name:
            messagebox.showwarning("Missing Info", "Member ID and Name are required.")
            return
        if member_id in self.members:
            messagebox.showwarning("Duplicate", "A member with this ID already exists.")
            return

        self.members[member_id] = Member(member_id, name)
        messagebox.showinfo("Success", f'Member "{name}" added.')

        self.member_id_var.set("")
        self.name_var.set("")

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for member in self.members.values():
            borrowed = ", ".join(member.borrowed_books) if member.borrowed_books else "-"
            self.tree.insert("", "end", values=(member.member_id, member.name, borrowed))


# ---------------------------------------------------------------------------
# Issue / Return tab
# ---------------------------------------------------------------------------

class IssueReturnTab(ttk.Frame):
    def __init__(self, parent, library, members, books_tab):
        super().__init__(parent, padding=10)
        self.library = library
        self.members = members
        self.books_tab = books_tab  # so we can refresh the Books tab's table after a change

        form = ttk.LabelFrame(self, text="Issue or Return a Book", padding=10)
        form.pack(fill="x")

        self.member_id_var = tk.StringVar()
        self.isbn_var = tk.StringVar()

        ttk.Label(form, text="Member ID:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(form, textvariable=self.member_id_var).grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Label(form, text="Book ISBN:").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(form, textvariable=self.isbn_var).grid(row=1, column=1, sticky="ew", pady=5)
        form.columnconfigure(1, weight=1)

        button_row = ttk.Frame(form)
        button_row.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(button_row, text="Issue Book", command=self.do_issue).pack(side="left", padx=5)
        ttk.Button(button_row, text="Return Book", command=self.do_return).pack(side="left", padx=5)

    def _get_member(self):
        member_id = self.member_id_var.get().strip()
        member = self.members.get(member_id)
        if member is None:
            messagebox.showerror("Member Not Found", f"No member with ID '{member_id}'.")
        return member

    def do_issue(self):
        member = self._get_member()
        if member is None:
            return
        isbn = self.isbn_var.get().strip()

        if issue_book(self.library, isbn, member):
            messagebox.showinfo("Success", "Book issued successfully.")
        else:
            messagebox.showerror("Failed", "Book unavailable or ISBN not found.")

        self.books_tab.refresh()

    def do_return(self):
        member = self._get_member()
        if member is None:
            return
        isbn = self.isbn_var.get().strip()

        if return_book(self.library, isbn, member):
            messagebox.showinfo("Success", "Book returned successfully.")
        else:
            messagebox.showerror("Failed", "This member did not have that book borrowed.")

        self.books_tab.refresh()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    library = Library()
    members = {}
    user_db = {}
    seed_demo_data(library, members, user_db)

    login = LoginWindow(library, members, user_db)
    login.mainloop()


if __name__ == "__main__":
    main()
