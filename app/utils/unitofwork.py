from app.db.database import async_session_maker
from app.repositories.authors import AuthorRepository
from app.repositories.books import BookRepository
from app.repositories.borrows import BorrowRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.author = AuthorRepository(self.session)
        self.book = BookRepository(self.session)
        self.borrow = BorrowRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
