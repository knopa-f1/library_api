from app.api.schemas.borrows import BorrowCreate, BorrowFromDB
from app.utils.exceptions import NotEnoughBooksError, ItemNotFoundError
from app.utils.unitofwork import UnitOfWork


class BorrowService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def add_borrow(self, borrow: BorrowCreate) -> BorrowFromDB:
        data_dict: dict = borrow.model_dump()  # prepare data
        async with self.uow:  # entrance to context
            book_id = data_dict['book_id']
            await self.uow.book.change_count(book_id, 1)
            borrow_to_return = await self.uow.borrow.add_one(data_dict)
            await self.uow.commit()
            return borrow_to_return

    async def get_borrows(self) -> list[BorrowFromDB]:
        async with self.uow:
            borrows: list = await self.uow.borrow.find_all()
            return [BorrowFromDB.model_validate(borrow) for borrow in borrows]

    async def get_borrow(self, borrow_id: int) -> BorrowFromDB | None:
        async with self.uow:
            borrow = await self.uow.borrow.get(borrow_id)
            return BorrowFromDB.model_validate(borrow)

    async def return_borrow(self, borrow_id: int) -> None:
        async with self.uow:
            borrow = await self.uow.borrow.return_book(borrow_id)
            await self.uow.book.change_count(borrow.book_id, -1)
            await self.uow.commit()
