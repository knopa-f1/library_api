from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    name: str
    description: str
    author_id: int
    count: int


class BookFromDB(BookCreate):
    model_config = ConfigDict(from_attributes=True)  # can be not only dict, also the objects

    id: int
