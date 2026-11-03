"""Core library operations and JSON storage. This module has no input/print code."""

from __future__ import annotations

import json
from pathlib import Path

from models import Book, FacultyMember, Member, StudentMember


class LibraryError(Exception):
    """Raised when a library action cannot be completed."""


class StorageError(Exception):
    """Raised when saved JSON cannot safely be read."""


class Library:
    """A collection of Book and Member objects (composition)."""

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}
        self._members: dict[str, Member] = {}

    @property
    def books(self) -> tuple[Book, ...]:
        return tuple(sorted(self._books.values(), key=lambda book: book.book_id))

    @property
    def members(self) -> tuple[Member, ...]:
        return tuple(sorted(self._members.values(), key=lambda member: member.member_id))

    def add_book(self, book_id: str, title: str, author: str) -> Book:
        book = Book(book_id, title, author)
        if book.book_id in self._books:
            raise LibraryError(f"Book ID '{book.book_id}' already exists.")
        self._books[book.book_id] = book
        return book

    def register_member(self, member_type: str, member_id: str, name: str) -> Member:
        member_type = member_type.strip().lower()
        types = {"student": StudentMember, "faculty": FacultyMember}
        if member_type not in types:
            raise LibraryError("Member type must be 'student' or 'faculty'.")
        member = types[member_type](member_id, name)
        if member.member_id in self._members:
            raise LibraryError(f"Member ID '{member.member_id}' already exists.")
        self._members[member.member_id] = member
        return member

    def get_book(self, book_id: str) -> Book:
        try:
            return self._books[book_id.strip()]
        except (KeyError, AttributeError):
            raise LibraryError(f"Book ID '{book_id}' was not found.") from None

    def get_member(self, member_id: str) -> Member:
        try:
            return self._members[member_id.strip()]
        except (KeyError, AttributeError):
            raise LibraryError(f"Member ID '{member_id}' was not found.") from None

    def search_books(self, query: str) -> tuple[Book, ...]:
        if not isinstance(query, str) or not query.strip():
            raise LibraryError("Search text cannot be blank.")
        query = query.strip().casefold()
        return tuple(book for book in self.books if query in book.title.casefold() or query in book.author.casefold())

    def borrow_book(self, book_id: str, member_id: str) -> None:
        book = self.get_book(book_id)
        member = self.get_member(member_id)
        if not book.is_available:
            raise LibraryError("This book is already borrowed.")
        # Polymorphism: the subclass decides its own limit.
        if len(member.borrowed_book_ids) >= member.borrow_limit():
            raise LibraryError(f"{member.name} has reached the borrowing limit of {member.borrow_limit()}.")
        book.lend_to(member.member_id)
        member.add_loan(book.book_id)

    def return_book(self, book_id: str, member_id: str) -> None:
        book = self.get_book(book_id)
        member = self.get_member(member_id)
        if book.borrower_id != member.member_id:
            raise LibraryError("This book can only be returned by the member who borrowed it.")
        book.return_from(member.member_id)
        member.remove_loan(book.book_id)

    def to_dict(self) -> dict:
        return {
            "books": [{"book_id": b.book_id, "title": b.title, "author": b.author, "borrower_id": b.borrower_id} for b in self.books],
            "members": [{"member_id": m.member_id, "name": m.name, "type": "student" if isinstance(m, StudentMember) else "faculty", "borrowed_book_ids": list(m.borrowed_book_ids)} for m in self.members],
        }

    def save(self, path: Path) -> None:
        path = Path(path)
        temporary = path.with_suffix(path.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(self.to_dict(), indent=2) + "\n", encoding="utf-8")
            temporary.replace(path)
        except OSError as error:
            raise StorageError(f"Could not save data: {error}") from error

    @classmethod
    def load(cls, path: Path) -> "Library":
        path = Path(path)
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise StorageError(f"Saved data is invalid and was not changed: {error}") from error
        if not isinstance(raw, dict) or not isinstance(raw.get("books"), list) or not isinstance(raw.get("members"), list):
            raise StorageError("Saved data is invalid and was not changed: books and members must be lists.")
        library = cls()
        try:
            for item in raw["books"]:
                library.add_book(item["book_id"], item["title"], item["author"])
            for item in raw["members"]:
                library.register_member(item["type"], item["member_id"], item["name"])
            for item in raw["books"]:
                if item.get("borrower_id") is not None:
                    library.borrow_book(item["book_id"], item["borrower_id"])
            expected = {item["member_id"]: sorted(item.get("borrowed_book_ids", [])) for item in raw["members"]}
            actual = {member.member_id: list(member.borrowed_book_ids) for member in library.members}
            if expected != actual:
                raise ValueError("member loan lists do not match book loans")
        except (KeyError, TypeError, ValueError, LibraryError) as error:
            raise StorageError(f"Saved data is inconsistent and was not changed: {error}") from error
        return library
