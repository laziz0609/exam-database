from datetime import datetime
from typing import Optional

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    Mapped,
    relationship,
)
from sqlalchemy import String, Boolean, ForeignKey, Text, DateTime, func, Integer, text


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


    def __repr__(self):
        return f"Author(id={self.id}, name={self.name}, craated_at={self.created_at})"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    published_year: Mapped[int] = mapped_column(Integer, nullable=False)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="book")


    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, published_year={self.published_year}, author_id={self.author_id}, is_available={self.is_available}, created_at={self.created_at}, updated_at={self.updated_at})"


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    grade: Mapped[str] = mapped_column(String(20))
    registered_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="student")


    def __repr__(self):
        return f"Student(id={self.id}, full_name={self.full_name}, email={self.email}, grade={self.grade}, registered_at={self.registered_at})"

class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    due_date: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("NOW() + INTERVAL '14 day'"), nullable=False
    )
    returned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    student: Mapped["Student"] = relationship("Student", back_populates="borrows")
    book: Mapped["Book"] = relationship("Book", back_populates="borrows")


    def __repr__(self):
        return f"Borrow(id={self.id}, student_id={self.student_id}, book_id={self.book_id}, borrowed_at={self.borrowed_at}, due_date={self.due_date}, returned_at={self.returned_at})"