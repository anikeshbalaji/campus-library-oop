"""Classes that represent books and library members."""

from __future__ import annotations


def _required_text(value: str, label: str) -> str:
    """Return clean text or raise an understandable validation error."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} cannot be blank.")
    return value.strip()


class Book:
    """A book that may be borrowed by one member at a time."""

    def __init__(self, book_id: str, title: str, author: str) -> None:
        self.book_id = _required_text(book_id, "Book ID")
        self.title = _required_text(title, "Title")
        self.author = _required_text(author, "Author")
        self._borrower_id: str | None = None

    @property
    def borrower_id(self) -> str | None:
        return self._borrower_id

    @property
    def is_available(self) -> bool:
        return self._borrower_id is None

    def lend_to(self, member_id: str) -> None:
        if not self.is_available:
            raise ValueError("This book is already borrowed.")
        self._borrower_id = _required_text(member_id, "Member ID")

    def return_from(self, member_id: str) -> None:
        if self._borrower_id != member_id:
            raise ValueError("This book was not borrowed by that member.")
        self._borrower_id = None


class Member:
    """Base class shared by all types of library member."""

    def __init__(self, member_id: str, name: str) -> None:
        self.member_id = _required_text(member_id, "Member ID")
        self.name = _required_text(name, "Name")
        self._borrowed_book_ids: set[str] = set()

    @property
    def borrowed_book_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._borrowed_book_ids))

    def borrow_limit(self) -> int:
        raise NotImplementedError("Each member type must define a borrowing limit.")

    def add_loan(self, book_id: str) -> None:
        self._borrowed_book_ids.add(book_id)

    def remove_loan(self, book_id: str) -> None:
        self._borrowed_book_ids.remove(book_id)


class StudentMember(Member):
    """A student can borrow up to two books."""

    def borrow_limit(self) -> int:
        return 2


class FacultyMember(Member):
    """A faculty member can borrow up to four books."""

    def borrow_limit(self) -> int:
        return 4
