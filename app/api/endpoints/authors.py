from app.api.schemas.authors import AuthorFromDB, AuthorCreate
from app.services.authors import AuthorService
from app.utils.exceptions import ItemSuccessfullyDeleted, ItemSuccessfullyUpdated
from app.utils.unitofwork import UnitOfWork
from fastapi import APIRouter, Depends

authors_router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


async def get_author_service(uow: UnitOfWork = Depends(UnitOfWork)) -> AuthorService:
    return AuthorService(uow)


@authors_router.post("/", response_model=AuthorFromDB)
async def create_author(data: AuthorCreate, author_service: AuthorService = Depends(get_author_service)):
    return await author_service.add_author(data)


@authors_router.get("/{author_id}", response_model=AuthorFromDB)
async def get_author(author_id: int, author_service: AuthorService = Depends(get_author_service)):
    author = await author_service.get_author(author_id)
    return author


@authors_router.get("/", response_model=list[AuthorFromDB])
async def get_authors(author_service: AuthorService = Depends(get_author_service)):
    return await author_service.get_authors()


@authors_router.delete("/{author_id}")
async def delete_author(author_id: int, author_service: AuthorService = Depends(get_author_service)):
    await author_service.delete_author(author_id)
    return ItemSuccessfullyDeleted('author', {"id": author_id})


@authors_router.put("/{author_id}")
async def update_author(author_id: int, data: AuthorCreate,
                        author_service: AuthorService = Depends(get_author_service)):
    await author_service.update_author(author_id, data)
    return ItemSuccessfullyUpdated('author', {"id": author_id})
