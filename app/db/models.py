import datetime

from app.api.schemas.authors import AuthorFromDB
from app.api.schemas.books import BookFromDB
from app.api.schemas.borrows import BorrowFromDB

from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String,  nullable=False)
    last_name: Mapped[str] = mapped_column(String,  nullable=False)
    birthdate: Mapped[datetime.date] = mapped_column(DateTime, nullable=True)

    def to_pydantic_model(self) -> AuthorFromDB:
        return AuthorFromDB(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            birthdate=self.birthdate
        )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String,  nullable=False)
    description: Mapped[str] = mapped_column(String,  nullable=True)
    author_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("author.id", ondelete="RESTRICT"))
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def to_pydantic_model(self) -> BookFromDB:
        return BookFromDB(
            id=self.id,
            name=self.name,
            description=self.description,
            author_id=self.author_id,
            count=self.count
        )


class Borrow(Base):
    __tablename__ = "borrow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("book.id", ondelete="RESTRICT"))
    reader_name: Mapped[str] = mapped_column(String, nullable=False)
    borrow_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    return_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    def to_pydantic_model(self) -> BorrowFromDB:
        return BorrowFromDB(
            id=self.id,
            book_id=self.book_id,
            reader_name=self.reader_name,
            borrow_date=self.borrow_date,
            return_date=self.return_date
        )
