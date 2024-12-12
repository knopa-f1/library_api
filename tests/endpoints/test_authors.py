import pytest
from app.api.schemas.authors import AuthorCreate, AuthorFromDB
from app.services.authors import AuthorService
from app.utils.unitofwork import UnitOfWork
from httpx import AsyncClient

author_service = AuthorService(UnitOfWork())


# prepare test data


async def get_author_dict(update: bool = False) -> dict:
    author_dict = {
        "first_name": "Lando",
        "last_name": "Norris",
        "birthdate": '1999-01-01'
    }
    if update:
        author_dict['first_name'] = "Charles"
    return author_dict


async def prepare_author(author_dict: dict = None) -> AuthorFromDB:
    if not author_dict:
        author_dict = await get_author_dict()
    author = AuthorCreate.model_validate(author_dict)
    author_from_db: AuthorFromDB = await author_service.add_author(author)
    return author_from_db


@pytest.mark.asyncio
async def test_create_author(ac: AsyncClient):
    response = await ac.post("/authors/",
                             json=await get_author_dict()
                             )
    assert response.status_code == 200
    assert response.json().get("first_name") == "Lando"


@pytest.mark.asyncio
async def test_get_authors(ac: AsyncClient):
    response = await ac.get("/authors/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_author(ac: AsyncClient):
    author_from_db = await prepare_author()
    response = await ac.get(f"/authors/{author_from_db.id}")
    assert response.status_code == 200
    assert response.json().get("last_name") == "Norris"


@pytest.mark.asyncio
async def test_get_incorrect_author(ac: AsyncClient):
    response = await ac.get(f"/authors/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_author(ac: AsyncClient):
    author_from_db = await prepare_author()
    response = await ac.delete(f"/authors/{author_from_db.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_incorrect_author(ac: AsyncClient):
    response = await ac.delete(f"/authors/9999999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_author(ac: AsyncClient):
    author_from_db = await prepare_author()
    response = await ac.put(f"/authors/{author_from_db.id}",
                            json=await get_author_dict(True))
    update_author_from_db: AuthorFromDB = await author_service.get_author(author_from_db.id)
    assert response.status_code == 200
    assert update_author_from_db.first_name == "Charles"
