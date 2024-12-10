from app.utils.unitofwork import UnitOfWork


class BaseService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_item(self, item):
        data_dict: dict = item.model_dump()  # prepare data
        async with self.uow:  # entrance to context
            item_to_return = await self.uow.author.add_one(data_dict)
            await self.uow.commit()
            return item_to_return

    async def get_all_items(self) -> list[AuthorFromDB]:
        async with self.uow:
            authors: list = await self.uow.author.find_all()
            return [AuthorFromDB.model_validate(author) for author in authors]

    async def get_author(self, author_id: int) -> AuthorFromDB | None:
        async with self.uow:
            author = await self.uow.author.get(id=author_id)
            return None if not author else AuthorFromDB.model_validate(author)

    async def update_author(self, author_id: int, author: AuthorCreate) -> None:
        data_dict: dict = author.model_dump()  # prepare data
        async with self.uow:
            await self.uow.author.update(author_id, data_dict)
            await self.uow.commit()

    async def delete_author(self, author_id: int) -> None:
        async with self.uow:
            await self.uow.author.delete(id=author_id)
            await self.uow.commit()