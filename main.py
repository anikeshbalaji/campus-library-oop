"""Terminal user interface for the Campus Library Management System."""

from pathlib import Path

from library import Library, LibraryError, StorageError

DATA_FILE = Path(__file__).resolve().parent / "library_data.json"


def create_sample_library() -> Library:
    library = Library()
    library.add_book("B001", "The Clockwork Campus", "Mira Sen")
    library.add_book("B002", "The Friendly Robot", "A. K. Rao")
    library.add_book("B003", "Moonbase Study Guide", "Leena Das")
    library.register_member("student", "S001", "Asha Kumar")
    library.register_member("faculty", "F001", "Dr. Nila Roy")
    return library


def show_books(books) -> None:
    if not books:
        print("No books found.")
        return
    for book in books:
        status = "Available" if book.is_available else f"Borrowed by {book.borrower_id}"
        print(f"{book.book_id}: {book.title} — {book.author} ({status})")


def show_members(library: Library) -> None:
    if not library.members:
        print("No members registered.")
        return
    for member in library.members:
        books = ", ".join(member.borrowed_book_ids) or "None"
        print(f"{member.member_id}: {member.name} | Limit: {member.borrow_limit()} | Borrowed: {books}")


def menu() -> None:
    print("\nCampus Library Management System")
    print("1. Add book\n2. Register student or faculty member\n3. List all books with availability")
    print("4. Search books by title or author\n5. Borrow book\n6. Return book")
    print("7. List members and their borrowed books\n8. Show a member's borrowing limit\n0. Save and exit")


def run() -> None:
    if DATA_FILE.exists():
        try:
            library = Library.load(DATA_FILE)
            print("Loaded saved library data.")
        except StorageError as error:
            print(f"ERROR: {error}")
            print("The file was not overwritten. Fix or remove it before restarting.")
            return
    else:
        library = create_sample_library()
        library.save(DATA_FILE)
        print("Created fictional sample data.")

    while True:
        menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                library.add_book(input("Book ID: "), input("Title: "), input("Author: "))
                library.save(DATA_FILE)
                print("Book added and saved.")
            elif choice == "2":
                member = library.register_member(input("Type (student/faculty): "), input("Member ID: "), input("Name: "))
                library.save(DATA_FILE)
                print(f"{member.__class__.__name__} registered and saved.")
            elif choice == "3":
                show_books(library.books)
            elif choice == "4":
                show_books(library.search_books(input("Search title or author: ")))
            elif choice == "5":
                library.borrow_book(input("Book ID: "), input("Member ID: "))
                library.save(DATA_FILE)
                print("Book borrowed and saved.")
            elif choice == "6":
                library.return_book(input("Book ID: "), input("Member ID: "))
                library.save(DATA_FILE)
                print("Book returned and saved.")
            elif choice == "7":
                show_members(library)
            elif choice == "8":
                member = library.get_member(input("Member ID: "))
                print(f"{member.name}'s borrowing limit is {member.borrow_limit()}.")
            elif choice == "0":
                library.save(DATA_FILE)
                print("Library data saved. Goodbye!")
                return
            else:
                print("Invalid menu choice. Please enter a number from the menu.")
        except (ValueError, LibraryError, StorageError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    run()
