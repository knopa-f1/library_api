import datetime

from fastapi import HTTPException


class ItemNotFoundError(HTTPException):
    def __init__(self, model_name: str, item_filter: dict, status_code: int = 404):
        super().__init__(status_code=status_code, detail=f'Item not found: {model_name}, filter = {item_filter}')


class ItemSuccessfullyDeleted(HTTPException):
    def __init__(self, model_name: str, item_filter: dict, status_code: int = 200):
        super().__init__(status_code=status_code, detail=f'Item was deleted: {model_name}, filter = {item_filter}')


class ItemSuccessfullyUpdated(HTTPException):
    def __init__(self, model_name: str, item_filter: dict, status_code: int = 200):
        super().__init__(status_code=status_code, detail=f'Item was updated: {model_name}, filter = {item_filter}')


class NotEnoughBooksError(HTTPException):
    def __init__(self, item_filter: dict, status_code: int = 400):
        super().__init__(status_code=status_code, detail=f'Not enough books with filter = {item_filter}')


class BorrowSuccessfullyReturned(HTTPException):
    def __init__(self, item_filter: dict, status_code: int = 200):
        super().__init__(status_code=status_code, detail=f'Borrow with filter= {item_filter} was returned')


class BorrowAlreadyReturned(HTTPException):
    def __init__(self, item_filter: dict, return_date: datetime.datetime, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail=f'Borrow with filter= {item_filter} had been already returned {return_date}'
            )


class BorrowDateLaterThanReturn(HTTPException):
    def __init__(self, item_filter: dict, borrow_date: datetime.datetime,
                 return_date: datetime.datetime, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail=f'Borrow with filter= {item_filter} has  borrow_date={borrow_date} and tried to return {return_date}'
        )
