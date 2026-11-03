import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from library import Library, LibraryError, StorageError
from models import FacultyMember, StudentMember


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.library.add_book("B1", "Python Basics", "Ada Smith")
        self.library.add_book("B2", "Campus Tales", "Ravi Kumar")
        self.library.add_book("B3", "Data Notes", "Ada Smith")
        self.library.register_member("student", "S1", "Student One")
        self.library.register_member("faculty", "F1", "Faculty One")

    def test_successful_borrowing_and_returning(self):
        self.library.borrow_book("B1", "S1")
        self.assertFalse(self.library.get_book("B1").is_available)
        self.library.return_book("B1", "S1")
        self.assertTrue(self.library.get_book("B1").is_available)

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaises(LibraryError): self.library.add_book("B1", "Other", "Author")
        with self.assertRaises(LibraryError): self.library.register_member("student", "S1", "Other")

    def test_unavailable_book_and_state_unchanged(self):
        self.library.borrow_book("B1", "S1")
        with self.assertRaises(LibraryError): self.library.borrow_book("B1", "F1")
        self.assertEqual(self.library.get_book("B1").borrower_id, "S1")
        self.assertEqual(self.library.get_member("F1").borrowed_book_ids, ())

    def test_student_and_faculty_limits(self):
        self.library.borrow_book("B1", "S1")
        self.library.borrow_book("B2", "S1")
        with self.assertRaises(LibraryError): self.library.borrow_book("B3", "S1")
        for number in range(4, 7): self.library.add_book(f"B{number}", f"Title {number}", "Author")
        for number in range(3, 7): self.library.borrow_book(f"B{number}", "F1")
        self.assertEqual(self.library.get_member("F1").borrow_limit(), 4)

    def test_unknown_ids_and_wrong_returner(self):
        with self.assertRaises(LibraryError): self.library.borrow_book("NO", "S1")
        with self.assertRaises(LibraryError): self.library.borrow_book("B1", "NO")
        self.library.borrow_book("B1", "S1")
        with self.assertRaises(LibraryError): self.library.return_book("B1", "F1")
        self.assertEqual(self.library.get_book("B1").borrower_id, "S1")

    def test_case_insensitive_search(self):
        self.assertEqual([book.book_id for book in self.library.search_books("ADA")], ["B1", "B3"])
        self.assertEqual([book.book_id for book in self.library.search_books("campus")], ["B2"])

    def test_save_reload_preserves_types_and_loans(self):
        self.library.borrow_book("B1", "S1")
        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "data.json"
            self.library.save(data_file)
            loaded = Library.load(data_file)
        self.assertIsInstance(loaded.get_member("S1"), StudentMember)
        self.assertIsInstance(loaded.get_member("F1"), FacultyMember)
        self.assertEqual(loaded.get_book("B1").borrower_id, "S1")

    def test_malformed_data_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "data.json"
            data_file.write_text("{not valid json", encoding="utf-8")
            before = data_file.read_text(encoding="utf-8")
            with self.assertRaises(StorageError): Library.load(data_file)
            self.assertEqual(data_file.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
