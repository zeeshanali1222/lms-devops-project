from datetime import datetime, timedelta

class Book:
    def __init__(self, book_id, title, author, total_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def __str__(self):
        return f"[{self.book_id}] '{self.title}' by {self.author} (Available: {self.available_copies}/{self.total_copies})"


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = {}  # Format: {book_id: due_date}

    def __str__(self):
        return f"Member [{self.member_id}]: {self.name} (Borrowed: {len(self.borrowed_books)} books)"


class LibrarySystem:
    def __init__(self):
        self.books = {}
        self.members = {}

    def add_book(self, book_id, title, author, copies):
        if book_id in self.books:
            self.books[book_id].total_copies += copies
            self.books[book_id].available_copies += copies
        else:
            self.books[book_id] = Book(book_id, title, author, copies)
        print(f"Successfully added/updated: {self.books[book_id]}")

    def register_member(self, member_id, name):
        if member_id not in self.members:
            self.members[member_id] = Member(member_id, name)
            print(f"Registered member: {self.members[member_id]}")
        else:
            print(f"Member ID {member_id} already exists.")

    def issue_book(self, member_id, book_id, loan_days=14):
        # Validation checks
        if member_id not in self.members:
            print(f"Error: Member ID {member_id} not found.")
            return False
        if book_id not in self.books:
            print(f"Error: Book ID {book_id} not found.")
            return False

        member = self.members[member_id]
        book = self.books[book_id]

        if book_id in member.borrowed_books:
            print(f"Error: Member {member.name} has already borrowed this book.")
            return False

        if book.available_copies <= 0:
            print(f"Error: '{book.title}' is currently out of stock.")
            return False

        # Process Issue
        due_date = datetime.now() + timedelta(days=loan_days)
        book.available_copies -= 1
        member.borrowed_books[book_id] = due_date

        print(f"Success: '{book.title}' issued to {member.name}. Due date: {due_date.strftime('%Y-%m-%d')}")
        return True

    def return_book(self, member_id, book_id, fine_per_day=1.50):
        # Validation checks
        if member_id not in self.members:
            print(f"Error: Member ID {member_id} not found.")
            return False
        if book_id not in self.books:
            print(f"Error: Book ID {book_id} not found.")
            return False

        member = self.members[member_id]
        book = self.books[book_id]

        if book_id not in member.borrowed_books:
            print(f"Error: {member.name} did not borrow '{book.title}'.")
            return False

        # Process Return & Fine Calculation
        due_date = member.borrowed_books[book_id]
        return_date = datetime.now()
        fine = 0.0

        if return_date > due_date:
            overdue_days = (return_date - due_date).days
            fine = overdue_days * fine_per_day
            print(f"Notice: Book is overdue by {overdue_days} days. Fine incurred: ${fine:.2f}")

        book.available_copies += 1
        del member.borrowed_books[book_id]

        print(f"Success: '{book.title}' returned by {member.name}. Book is back in inventory.")
        return fine


# --- Example Usage ---
if __name__ == "__main__":
    # Initialize Library
    library = LibrarySystem()

    # Add inventory
    library.add_book("B001", "Python Crash Course", "Corvit", 2)
    library.add_book("B002", "AWS", "Hasnain Malik", 1)

    # Register members
    library.register_member("M001", "Ali")

    print("\n--- Testing Issue Workflow ---")
    library.issue_book("M001", "B001")  # Should succeed
    library.issue_book("M001", "B001")  # (already borrowed)
    
    print("\n--- Testing Return Workflow ---")
    library.return_book("M001", "B001")  # Should succeed
    