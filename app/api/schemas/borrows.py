import datetime

from pydantic import BaseModel, ConfigDict


class BorrowCreate(BaseModel):
    book_id: int
    reader_name: str
    borrow_date: datetime.datetime
    return_date: datetime.datetime|None = None


class BorrowFromDB(BorrowCreate):
    model_config = ConfigDict(from_attributes=True)  # can be not only dict, also the objects

    id: int
