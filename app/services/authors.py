from app.api.schemas.authors import AuthorCreate, AuthorFromDB
from app.utils.unitofwork import UnitOfWork


class AuthorService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_author(self, author: AuthorCreate) -> AuthorFromDB:
        data_dict: dict = author.model_dump()  # prepare data
        async with self.uow:  # entrance to context
            author_to_return = await self.uow.author.add_one(data_dict)
            await self.uow.commit()
            return author_to_return

    async def get_authors(self) -> list[AuthorFromDB]:
        async with self.uow:
            authors: list = await self.uow.author.find_all()
            return [AuthorFromDB.model_validate(author) for author in authors]

    async def get_author(self, author_id: int) -> AuthorFromDB | None:
        async with self.uow:
            author = await self.uow.author.get(author_id)
            return AuthorFromDB.model_validate(author)

    async def update_author(self, author_id: int, author: AuthorCreate) -> None:
        data_dict: dict = author.model_dump()  # prepare data
        async with self.uow:
            await self.uow.author.update(author_id, data_dict)
            await self.uow.commit()

    async def delete_author(self, author_id: int) -> None:
        async with self.uow:
            await self.uow.author.delete(author_id)
            await self.uow.commit()
