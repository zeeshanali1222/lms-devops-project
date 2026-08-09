"""
library_management_system.py - Group G: Main Application Interface

Purpose: Combine all modules together.
Responsibilities: Provide a user-friendly menu and actions.
"""

from book import Book
from member import Member
from library import Library
from issue_return import issue_book, return_book
from search import search_by_title, search_by_author, search_by_isbn
from auth_system import authenticate, register_user


def seed_demo_data(library, members, user_db):
    """Populate the system with a few demo books, members, and a user account."""
    library.add_book(Book("111", "Clean Code", "Robert C. Martin", 3))
    library.add_book(Book("222", "The Pragmatic Programmer", "David Thomas", 2))
    library.add_book(Book("333", "Introduction to Algorithms", "Thomas H. Cormen", 1))

    members["M001"] = Member("M001", "Alice Johnson")
    members["M002"] = Member("M002", "Bob Smith")

    user_db["admin"] = "admin123"


def print_menu():
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. List Books")
    print("3. Search Books")
    print("4. Add Member")
    print("5. Issue Book")
    print("6. Return Book")
    print("7. Exit")


def handle_add_book(library):
    isbn = input("ISBN: ").strip()
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    try:
        copies = int(input("Copies: ").strip())
    except ValueError:
        print("Copies must be a number.")
        return
    library.add_book(Book(isbn, title, author, copies))
    print(f"Book '{title}' added.")


def handle_list_books(library):
    books = library.list_books()
    if not books:
        print("No books in the library yet.")
        return
    for book in books:
        print(f" - {book}")


def handle_search(library):
    print("Search by: 1) Title  2) Author  3) ISBN")
    choice = input("Choose an option: ").strip()
    query = input("Enter search text: ").strip()
    if choice == "1":
        results = search_by_title(library, query)
    elif choice == "2":
        results = search_by_author(library, query)
    elif choice == "3":
        result = search_by_isbn(library, query)
        results = [result] if result else []
    else:
        print("Invalid choice.")
        return
    if not results:
        print("No matching books found.")
        return
    for book in results:
        print(f" - {book}")


def handle_add_member(members):
    member_id = input("Member ID: ").strip()
    name = input("Name: ").strip()
    members[member_id] = Member(member_id, name)
    print(f"Member '{name}' added.")


def handle_issue_book(library, members):
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    member = members.get(member_id)
    if member is None:
        print("Member not found.")
        return
    if issue_book(library, isbn, member):
        print("Book issued successfully.")
    else:
        print("Book unavailable or ISBN not found.")


def handle_return_book(library, members):
    member_id = input("Member ID: ").strip()
    isbn = input("Book ISBN: ").strip()
    member = members.get(member_id)
    if member is None:
        print("Member not found.")
        return
    if return_book(library, isbn, member):
        print("Book returned successfully.")
    else:
        print("This member did not have that book borrowed.")


def main():
    """Entry point for the interactive command-line Library Management System."""
    library = Library()
    members = {}
    user_db = {}
    seed_demo_data(library, members, user_db)

    print("Welcome to the Library Management System")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if not authenticate(username, password, user_db):
        print("Authentication failed. Exiting.")
        return

    print(f"Login successful. Welcome, {username}!")

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            handle_add_book(library)
        elif choice == "2":
            handle_list_books(library)
        elif choice == "3":
            handle_search(library)
        elif choice == "4":
            handle_add_member(members)
        elif choice == "5":
            handle_issue_book(library, members)
        elif choice == "6":
            handle_return_book(library, members)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
