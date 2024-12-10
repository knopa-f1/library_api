import datetime

from pydantic import BaseModel, ConfigDict


class AuthorCreate(BaseModel):
    first_name: str
    last_name: str
    birthdate: datetime.date


class AuthorFromDB(AuthorCreate):
    model_config = ConfigDict(from_attributes=True)  # can be not only dict, also the objects

    id: int
