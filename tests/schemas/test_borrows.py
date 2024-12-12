import pytest
from app.api.schemas.borrows import BorrowFromDB, BorrowCreate
import datetime


def test_borrow_create_model():
    borrow = BorrowCreate(book_id=1, reader_name="Carlos",
                          borrow_date=datetime.datetime(2024, 1, 1, 0, 0, 0))

    assert borrow.book_id == 1
    assert borrow.reader_name == "Carlos"
    assert borrow.borrow_date == datetime.datetime(2024, 1, 1, 0, 0, 0)
    assert borrow.return_date is None
    with pytest.raises(ValueError):
        BorrowCreate(book_id=1, reader_name="Carlos")


def test_book_from_db_model():
    borrow = BorrowFromDB(book_id=1, reader_name="Carlos", id=5,
                          borrow_date=datetime.datetime(2024, 1, 1, 0, 0, 0),
                          return_date=datetime.datetime(2024, 1, 2, 0, 0, 0))

    assert borrow.book_id == 1
    assert borrow.reader_name == "Carlos"
    assert borrow.borrow_date == datetime.datetime(2024, 1, 1, 0, 0, 0)
    assert borrow.return_date == datetime.datetime(2024, 1, 2, 0, 0, 0)
    with pytest.raises(ValueError):
        BorrowFromDB(book_id=1, reader_name="Carlos")
