from app.api.schemas.borrows import BorrowCreate, BorrowFromDB
from app.services.borrows import BorrowService
from app.utils.exceptions import BorrowSuccessfullyReturned
from app.utils.unitofwork import UnitOfWork
from fastapi import APIRouter, Depends

borrows_router = APIRouter(
    prefix="/borrows",
    tags=["Borrows"]
)


async def get_borrow_service(uow: UnitOfWork = Depends(UnitOfWork)) -> BorrowService:
    return BorrowService(uow)


@borrows_router.post("/", response_model=BorrowFromDB)
async def create_borrow(data: BorrowCreate, borrow_service: BorrowService = Depends(get_borrow_service)):
    return await borrow_service.add_borrow(data)


@borrows_router.get("/{borrow_id}", response_model=BorrowFromDB)
async def get_borrow(borrow_id: int, borrow_service: BorrowService = Depends(get_borrow_service)):
    borrow = await borrow_service.get_borrow(borrow_id)
    return borrow


@borrows_router.get("/", response_model=list[BorrowFromDB])
async def get_borrows(borrow_service: BorrowService = Depends(get_borrow_service)):
    return await borrow_service.get_borrows()


@borrows_router.patch("/{borrow_id}")
async def return_borrow(borrow_id: int, borrow_service: BorrowService = Depends(get_borrow_service)):
    await borrow_service.return_borrow(borrow_id)
    return BorrowSuccessfullyReturned({"id": borrow_id})

