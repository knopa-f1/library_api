from app.api.schemas.books import BookCreate, BookFromDB
from app.services.books import BookService
from app.utils.exceptions import ItemSuccessfullyDeleted, ItemSuccessfullyUpdated
from app.utils.unitofwork import UnitOfWork
from fastapi import APIRouter, Depends

books_router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


async def get_books_service(uow: UnitOfWork = Depends(UnitOfWork)) -> BookService:
    return BookService(uow)


@books_router.post("/", response_model=BookFromDB)
async def create_book(data: BookCreate, book_service: BookService = Depends(get_books_service)):
    return await book_service.add_book(data)


@books_router.get("/{book_id}", response_model=BookFromDB)
async def get_book(book_id: int, book_service: BookService = Depends(get_books_service)):
    book = await book_service.get_book(book_id)
    return book


@books_router.get("/", response_model=list[BookFromDB])
async def get_books(book_service: BookService = Depends(get_books_service)):
    return await book_service.get_books()


@books_router.delete("/{book_id}")
async def delete_book(book_id: int, book_service: BookService = Depends(get_books_service)):
    await book_service.delete_book(book_id)
    return ItemSuccessfullyDeleted('book', {"id": book_id})


@books_router.put("/{book_id}")
async def update_book(book_id: int, data: BookCreate, book_service: BookService = Depends(get_books_service)):
    await book_service.update_book(book_id, data)
    return ItemSuccessfullyUpdated('book', {"id": book_id})
