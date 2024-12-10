from app.api.schemas.books import BookCreate, BookFromDB
from app.utils.unitofwork import UnitOfWork


class BookService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_book(self, book: BookCreate) -> BookFromDB:
        data_dict: dict = book.model_dump()  # prepare data
        async with self.uow:  # entrance to context
            author = await self.uow.author.get(data_dict['author_id'])
            if author:
                book_to_return = await self.uow.book.add_one(data_dict)
            await self.uow.commit()
            return book_to_return

    async def get_books(self) -> list[BookFromDB]:
        async with self.uow:
            books: list = await self.uow.book.find_all()
            return [BookFromDB.model_validate(book) for book in books]

    async def get_book(self, book_id: int) -> BookFromDB | None:
        async with self.uow:
            book = await self.uow.book.get(book_id)
            return BookFromDB.model_validate(book)

    async def update_book(self, book_id: int, book: BookFromDB) -> None:
        data_dict: dict = book.model_dump()  # prepare data
        async with self.uow:
            author = await self.uow.author.get(data_dict['author_id'])
            if author:
                await self.uow.book.update(book_id, data_dict)
                await self.uow.commit()

    async def delete_book(self, book_id: int) -> None:
        async with self.uow:
            await self.uow.book.delete(book_id)
            await self.uow.commit()
