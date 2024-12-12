import pytest
from app.api.schemas.books import BookCreate, BookFromDB
import datetime


def test_book_create_model():
    book = BookCreate(name="Aston Martin", description="", author_id=1, count=5)

    assert book.name == "Aston Martin"
    assert book.description == ""
    assert book.author_id == 1
    assert book.count==5
    with pytest.raises(ValueError):
        BookCreate(name="Aston Martin", description="", author_id=1, count=5.5)


def test_book_from_db_model():
    book = BookFromDB(name="Aston Martin", description="", author_id=1, count=5, id=1)

    assert book.name == "Aston Martin"
    assert book.description == ""
    assert book.author_id == 1
    assert book.count == 5
    assert book.id == 1
    with pytest.raises(ValueError):
        BookFromDB(name="Aston Martin", description="", author_id=1, count=5, id='a')