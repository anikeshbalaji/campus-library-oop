# Viva Notes — Campus Library Management System

## Class roles

- `Book` stores a book ID, title, author, and its current borrower. Its `is_available` property derives availability from whether a borrower exists.
- `Member` is the common base class for every library member. It stores an ID, name, and borrowed book IDs.
- `StudentMember` is a `Member` with a limit of 2 books.
- `FacultyMember` is a `Member` with a limit of 4 books.
- `Library` contains all books and members and applies the borrowing, return, search, validation, save, and load rules.

## `self` and `__init__`

`self` means the current object. For example, `self.title` means the title belonging to one particular book. `__init__` is a constructor: Python runs it when an object is created, so it gives that object its starting values.

## Inheritance and overriding

`StudentMember(Member)` and `FacultyMember(Member)` inherit the ID, name, and loan-list behavior from `Member`. They override `borrow_limit()` by writing their own version of that method: student returns `2`, faculty returns `4`.

## Polymorphism

In `Library.borrow_book()`, the program calls `member.borrow_limit()`. It does not use an `if student` or `if faculty` condition. Python chooses the correct overridden method based on the actual object. This is polymorphism.

## Encapsulation and composition

Internal attributes such as `Book._borrower_id` and `Member._borrowed_book_ids` begin with `_`. Public methods validate changes instead of allowing direct updates. The underscore is a convention, not a password or security feature.

Composition means one object contains other objects. The `Library` object contains dictionaries of `Book` and `Member` objects.

## Borrowing, returning, and JSON

When borrowing, the library first finds both IDs, checks availability, and checks the member's polymorphic limit. It then records the same loan in the book and member. When returning, only the recorded borrower can return the book. JSON saves book details, member type, and borrower information. On loading, the program rebuilds the correct subclasses and checks that the saved loan records agree.

## Ten likely questions

1. **Why use a base `Member` class?**  It keeps shared data and behavior in one place.
2. **Why are there subclasses?**  Students and faculty have different borrowing limits.
3. **What is method overriding?**  A subclass provides its own version of an inherited method.
4. **Where is polymorphism used?**  `member.borrow_limit()` works correctly for either subclass.
5. **Why is availability a property?**  It is derived from borrower data, so no separate value can get out of sync.
6. **What prevents duplicate IDs?**  `Library` checks its internal dictionaries before adding an object.
7. **What happens if a book is already borrowed?**  The borrow action raises `LibraryError` and changes nothing.
8. **Why are input and print statements in `main.py`?**  This keeps the reusable rules in `library.py` easy to test.
9. **Why use `pathlib`?**  It builds a path relative to the project file in a readable, cross-platform way.
10. **Why is malformed JSON not overwritten?**  Overwriting could destroy data that might be repaired, so the program exits safely.
