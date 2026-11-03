# Campus Library Management System

**Assessment 5 — Python Object-Oriented Programming**

| Student | Details |
| --- | --- |
| Name | T M ANIKESH BALAJI |
| Registration number | 26BCE1718 |
| Institution | VIT Chennai |

## Objective

This beginner-friendly terminal application manages a small campus library. It demonstrates Python classes, objects, encapsulation, inheritance, polymorphism, composition, validation, JSON file storage, and unit testing using only the standard library.

## Features

- Add and search books; searches ignore upper/lower case.
- Register student and faculty members.
- Borrow and return books with availability and borrower checks.
- Student limit: 2 books; faculty limit: 4 books.
- Save books, member types, and loans to local JSON after successful changes.
- Load existing data on the next start. First use creates fictional sample data.
- Reject duplicate or blank information and handle bad menu input safely.

## Run

Use Python 3.10 or later. From this folder:

```sh
python main.py
```

On systems where `python` means Python 2 or is unavailable:

```sh
python3 main.py
```

`library_data.json` is created beside `main.py`, so the program works even when launched from another terminal folder. It is ignored by Git because it is local runtime data.

## Test

```sh
python -m unittest discover -s tests -v
```

Or:

```sh
python3 -m unittest discover -s tests -v
```

The tests use temporary directories and never change the real runtime JSON file.

## File structure

```text
campus-library-oop/
├── main.py             # menu and input/output only
├── models.py           # Book and Member classes
├── library.py          # library rules and JSON storage
├── tests/test_library.py
├── README.md
├── VIVA.md
└── .gitignore
```

## OOP mapping

| Concept | Where it appears |
| --- | --- |
| Classes and objects | `Book`, `Member`, `Library`, and their created objects |
| Constructors | Each class's `__init__` method sets initial data |
| Encapsulation | `_borrower_id`, `_borrowed_book_ids`, and validated methods such as `lend_to()` |
| Inheritance | `StudentMember` and `FacultyMember` inherit from `Member` |
| Polymorphism | `Library.borrow_book()` calls `member.borrow_limit()` without testing the member type |
| Composition | `Library` contains dictionaries of `Book` and `Member` objects |

An underscore is a Python convention that says an attribute is internal. It helps communicate intent, but it is not a security control: Python does not make it truly private.

## Example session

```text
Created fictional sample data.
Choose an option: 5
Book ID: B001
Member ID: S001
Book borrowed and saved.

Choose an option: 8
Member ID: S001
Asha Kumar's borrowing limit is 2.

Choose an option: 0
Library data saved. Goodbye!
```

## Persistence and safety

The program writes JSON only after a successful add, registration, borrow, or return, and again on normal exit. It writes a temporary file and replaces the old file only when that write succeeds. If the existing JSON is malformed or its loans are inconsistent, the program clearly reports the problem and exits without overwriting the file.

## Limitations

This is a local, single-user educational application. It has no login, network sharing, database server, reservations, due dates, or fine calculation.

## AI assistance acknowledgement

This project was developed with AI assistance for structure, explanations, implementation, and testing. The student should read, run, and understand the code before submission and be ready to explain it in the viva.
