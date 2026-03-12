from library.db import engine, SessionLocal
from library.models import Base, Author, Book, Student, Borrow

from library.services import AuthorService, BookService, StudentService, BorrowService, StatisticService


def create_tables():
    Base.metadata.create_all(bind=engine)


# create_tables()
session = SessionLocal()



author_serv = AuthorService(session)
def create_author():
    return author_serv.create_author("Erkin vohidov1", "ko'plab mashhur asarlar sohibi")

def get_author(id):
    return author_serv.get_author_by_id(id)

def all_author():
    return author_serv.get_all_authors()

def update_author(author_id: int, name: str = None, bio: str = None):
    return author_serv.update_author(author_id, name, bio)

def delate_author(author_id: int):
    return author_serv.delete_author(author_id)
# print(create_author())
# print(get_author(76))
# print(all_author())
# # print(update_author(author_id= 1, bio = "ko'plab mashhur asarlar sohibi"))
# print(delate_author(43))
# print(all_author())


book_serv = BookService(session)

def create_book():
    return book_serv.create_book("hujramda", 1, 2033, "fasfas")

def get_book(id):
    return book_serv.get_book_by_id(id)

def all_book():
    return book_serv.get_all_books()

def update_book(book_id: int, title: str = None, author_id: int = None, published_year: int = None, isbn: str = None):
    return book_serv.update_book(book_id, title, author_id, published_year, isbn)

def delate_book(book_id: int):
    return book_serv.delete_book(book_id)
# print(create_book())
# print(get_book(1))
# print(all_book())
# print(update_book(book_id= 1, title = "test2", isbn= "123vfd6"))
# print(delate_book(2))
# print(all_book())


student_serv = StudentService(session)

def create_student():
    return student_serv.create_student("test testova", "test1.@coma", "test1")

# print(create_student())


borrow_serv = BorrowService(session)

def borrow_book():
    return borrow_serv.borrow_book(1, 4)

def return_book():
    return borrow_serv.return_book(1)

print(borrow_book())
# print(return_book())


statistic_serv = StatisticService(session)

def get_student_borrow_count():
    return statistic_serv.get_student_borrow_count(31)

def get_currently_borrowed_books():
    return statistic_serv.get_currently_borrowed_books()

def get_books_by_author():
    return statistic_serv.get_books_by_author(1)

def get_overdue_borrows():
    return statistic_serv.get_overdue_borrows()

# print(get_student_borrow_count())
# print(get_currently_borrowed_books())
# print(get_books_by_author())
print(get_overdue_borrows())