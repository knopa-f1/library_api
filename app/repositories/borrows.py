from datetime import datetime

from app.db.models import Borrow
from app.api.schemas.borrows import BorrowFromDB
from app.repositories.base_repository import Repository
from app.utils.exceptions import ItemNotFoundError, BorrowAlreadyReturned, BorrowDateLaterThanReturn


class BorrowRepository(Repository):
    model = Borrow

    async def return_book(self, borrow_id: int) -> BorrowFromDB:
        borrow = await self.get(borrow_id)
        if borrow:
            return_date = datetime.now()
            if borrow.return_date:
                raise BorrowAlreadyReturned({'id': borrow_id}, borrow.return_date)
            elif return_date.timestamp() < borrow.borrow_date.timestamp():
                raise BorrowDateLaterThanReturn({'id': borrow_id}, borrow.borrow_date, return_date)
            borrow.return_date = return_date
        else:
            raise ItemNotFoundError("borrow", {'id': borrow_id})
        return borrow
