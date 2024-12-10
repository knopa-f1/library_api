from abc import ABC, abstractmethod

from app.utils.exceptions import ItemNotFoundError
from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as upsert


# class AbstractRepository(ABC):
#     @abstractmethod
#     async def add_one(self, data: dict):
#         raise NotImplementedError
#
#     @abstractmethod
#     async def find_all(self):
#         raise NotImplementedError


class Repository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one().to_pydantic_model()

    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def find_one(self, **filter_by) -> BaseModel:
        stmt = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(stmt)
        try:
            result = result.scalar_one().to_pydantic_model()
        except NoResultFound:
            raise ItemNotFoundError(self.model.__tablename__, filter_by)
        return result

    async def get(self, record_id: int):
        result = await self.session.get(self.model, record_id)
        if not result:
            raise ItemNotFoundError(self.model.__tablename__, {'id': record_id})
        return result

    async def update(self, record_id: int, data: dict) -> None:
        data["id"] = record_id
        stmt = upsert(self.model).values(
            data
        ).on_conflict_do_update(
            index_elements=['id'],
            set_=data
        )

        result = await self.session.execute(stmt)

    async def delete(self, record_id: int) -> None:
        item = await self.get(record_id)
        if not item:
            raise ItemNotFoundError(self.model.__tablename__, {'id': record_id})
        await self.session.delete(item)
