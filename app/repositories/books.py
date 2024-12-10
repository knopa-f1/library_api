from app.db.models import Book
from app.repositories.base_repository import Repository
from app.utils.exceptions import NotEnoughBooksError, ItemNotFoundError


class BookRepository(Repository):
    model = Book

    async def change_count(self, book_id: int, count :int = 1):
        book = await self.get(book_id)
        if book:
            if book.count <= 0:
                raise NotEnoughBooksError({'book_id': book_id})
            book.count -= count
        else:
            raise ItemNotFoundError("book", {'book_id': book_id})
