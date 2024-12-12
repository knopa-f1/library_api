import pytest
from app.api.schemas.authors import AuthorFromDB
from app.api.schemas.books import BookCreate, BookFromDB
from app.services.books import BookService
from app.utils.unitofwork import UnitOfWork
from httpx import AsyncClient
from tests.endpoints.test_authors import prepare_author

book_service = BookService(UnitOfWork())


# prepare test data


async def get_book_dict(update: bool = False, count: int = 1) -> dict:
    author_from_db: AuthorFromDB = await prepare_author()
    book_dict = {
        "name": "Champions",
        "description": "McLaren",
        "author_id": author_from_db.id,
        'count': count
    }
    if update:
        book_dict['description'] = "McLaren F1"
    return book_dict


async def prepare_book(count: int = 1) -> BookFromDB:
    book = BookCreate.model_validate(await get_book_dict(count=count))
    book_from_db: BookFromDB = await book_service.add_book(book)
    return book_from_db


@pytest.mark.asyncio
async def test_create_book(ac: AsyncClient):
    response = await ac.post("/books/",
                             json=await get_book_dict()
                             )

    assert response.status_code == 200
    assert response.json().get("description") == "McLaren"


@pytest.mark.asyncio
async def test_get_books(ac: AsyncClient):
    response = await ac.get("/books/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_book(ac: AsyncClient):
    book_from_db = await prepare_book()
    response = await ac.get(f"/books/{book_from_db.id}")
    assert response.status_code == 200
    assert response.json().get("description") == "McLaren"


@pytest.mark.asyncio
async def test_get_incorrect_book(ac: AsyncClient):
    response = await ac.get(f"/books/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_book(ac: AsyncClient):
    book_from_db = await prepare_book()
    response = await ac.delete(f"/books/{book_from_db.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_incorrect_book(ac: AsyncClient):
    response = await ac.delete(f"/books/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_book(ac: AsyncClient):
    book_from_db = await prepare_author()
    response = await ac.put(f"/books/{book_from_db.id}",
                            json=await get_book_dict(True))
    update_book_from_db: BookFromDB = await book_service.get_book(book_from_db.id)
    assert response.status_code == 200
    assert update_book_from_db.description == "McLaren F1"
