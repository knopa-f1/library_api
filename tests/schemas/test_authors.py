import pytest
from app.api.schemas.authors import AuthorCreate, AuthorFromDB
import datetime


def test_author_create_model():
    author = AuthorCreate(first_name="Fernando", last_name="Alonso", birthdate=datetime.date(1985, 1, 1))

    assert author.first_name == "Fernando"
    assert author.last_name == "Alonso"
    assert author.birthdate == datetime.date(1985, 1, 1)
    with pytest.raises(ValueError):
        AuthorCreate(first_name="Fernando", last_name="Alonso")


def test_author_from_db_model():
    author = AuthorFromDB(first_name="Fernando", last_name="Alonso", birthdate=datetime.date(1985, 1, 1), id=1)

    assert author.first_name == "Fernando"
    assert author.last_name == "Alonso"
    assert author.birthdate == datetime.date(1985, 1, 1)
    assert author.id == 1
    with pytest.raises(ValueError):
        AuthorFromDB(first_name="Fernando", last_name="Alonso", birthdate=datetime.date(1985, 1, 1))
