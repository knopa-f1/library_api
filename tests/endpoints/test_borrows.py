import datetime

import pytest
from app.api.schemas.books import BookFromDB
from app.api.schemas.borrows import BorrowCreate, BorrowFromDB
from app.services.borrows import BorrowService
from app.utils.unitofwork import UnitOfWork
from httpx import AsyncClient
from tests.endpoints.test_books import prepare_book, book_service

borrow_service = BorrowService(UnitOfWork())


# prepare test data


async def get_borrow_info(borrow_date: datetime = datetime.datetime.now(), initial_count: int = 1, ) -> dict:
    book_from_db: BookFromDB = await prepare_book(count=initial_count)
    print(book_from_db)
    borrow_dict = {
        "book_id": book_from_db.id,
        "reader_name": "Lewis",
        "borrow_date": borrow_date.isoformat()
    }

    return {
        'borrow_dict': borrow_dict,
        'book_count': book_from_db.count
    }


async def prepare_borrow(borrow_date: datetime = datetime.datetime.now()) -> dict:
    borrow_info = await get_borrow_info(borrow_date=borrow_date)
    borrow = BorrowCreate.model_validate(borrow_info['borrow_dict'])
    borrow_from_db: BorrowFromDB = await borrow_service.add_borrow(borrow)
    return {
        'borrow_from_db': borrow_from_db,
        'book_count': borrow_info['book_count']
    }


# tests

@pytest.mark.asyncio
async def test_create_borrow(ac: AsyncClient):
    borrow_info = await get_borrow_info()
    response = await ac.post("/borrows/",
                             json=borrow_info['borrow_dict']
                             )
    book_from_db: BookFromDB = await book_service.get_book(borrow_info['borrow_dict']['book_id'])

    assert response.status_code == 200
    assert response.json().get("reader_name") == "Lewis"
    assert book_from_db.count == borrow_info['book_count'] - 1


@pytest.mark.asyncio
async def test_create_incorrect_borrow(ac: AsyncClient):
    borrow_info = await get_borrow_info(initial_count=0)
    response = await ac.post("/borrows/",
                             json=borrow_info['borrow_dict']
                             )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_borrows(ac: AsyncClient):
    response = await ac.get("/borrows/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_borrow(ac: AsyncClient):
    borrow_info = await prepare_borrow()
    response = await ac.get(f"/borrows/{borrow_info['borrow_from_db'].id}")
    assert response.status_code == 200
    assert response.json().get("reader_name") == "Lewis"


@pytest.mark.asyncio
async def test_get_incorrect_borrow(ac: AsyncClient):
    response = await ac.get(f"/borrows/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_return_borrow(ac: AsyncClient):
    borrow_info = await prepare_borrow()
    response = await ac.patch(f"/borrows/{borrow_info['borrow_from_db'].id}")
    borrow_from_db: BorrowFromDB = await borrow_service.get_borrow(borrow_info['borrow_from_db'].id)
    book_from_db: BookFromDB = await book_service.get_book(borrow_info['borrow_from_db'].book_id)
    assert response.status_code == 200
    assert book_from_db.count == borrow_info['book_count']
    assert datetime.datetime.date(borrow_from_db.return_date) == datetime.datetime.today().date()


@pytest.mark.asyncio
async def test_return_incorrect_borrow(ac: AsyncClient):
    borrow_date = datetime.datetime.now().now() + datetime.timedelta(days=1)
    borrow_info = await prepare_borrow(borrow_date=borrow_date)
    response = await ac.patch(f"/borrows/{borrow_info['borrow_from_db'].id}")
    assert response.status_code == 400
