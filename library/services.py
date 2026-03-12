from datetime import datetime

from sqlalchemy.orm import Session

from library.models import Author, Book, Student, Borrow



class AuthorService:
    def __init__(self, sessin: Session):
        self.session = sessin

    def create_author(self, name: str, bio: str = None) -> Author:
        """Yangi muallif yaratish"""

        author = Author(name = name, bio = bio)
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)

        return author
        

    def get_author_by_id(self, author_id: int) -> Author | None:
        """ID bo'yicha muallifni olish"""

        return self.session.query(Author).get(author_id)
         

    def get_all_authors(self) -> list[Author]:
        """Barcha mualliflar ro'yxatini olish"""

        authors = self.session.query(Author).all()
        return authors


    def update_author(self, author_id: int, name: str = None, bio: str = None) -> Author | None:
        """Muallif ma'lumotlarini yangilash"""

        author = self.session.query(Author).get(author_id)
        if not author:
            return None
        
        if name: 
            author.name = name
        if bio:
            author.bio = bio

        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)

        return author


    def delete_author(self, author_id: int) -> bool:
        """Muallifni o'chirish (faqat kitoblari bo'lmagan holda)"""
        
        author = self.session.query(Author).get(author_id)
        if not author:
            return False
        
        self.session.delete(author)
        self.session.commit()
        return True
    


class BookService:
    def __init__(self, sessin: Session):
        self.session = sessin

    
    def create_book(self, title: str, author_id: int, published_year: int, isbn: str = None) -> Book | None:
        """Yangi kitob yaratish"""
        if isbn:
            check_book = self.session.query(Book).filter(Book.isbn == isbn).first()
            if check_book:
                raise ValueError("Book with this ISBN already exists")
            
        if published_year < 0 or published_year > datetime.now():
            return None
        
        book = Book(title = title, author_id = author_id, published_year = published_year, isbn = isbn)
        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)

        return book
    
    def get_book_by_id(self, book_id: int) -> Book | None:
        """ID bo'yicha kitobni olish"""
        
        book = self.session.query(Book).get(book_id)
        return book

    def get_all_books(self) -> list[Book]:
        """Barcha kitoblar ro'yxatini olish"""

        books = self.session.query(Book).all()
        return books

    def search_books_by_title(self, title: str) -> list[Book]:
        """Kitoblarni sarlavha bo'yicha qidirish (partial match)"""
        books = self.session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

        return books

    def delete_book(self, book_id: int) -> bool:
        """Kitobni o'chirish"""
        
        book = self.session.query(Book).get(book_id)
        if not book:
            return False
        
        self.session.delete(book)
        self.session.commit()
        return True
    

    def update_book(self, book_id: int, title: str = None, author_id: int = None, published_year: int = None, isbn: str = None) -> Book | None:
        """Kitob ma'lumotlarini yangilash"""
        if isbn:
            check_book = self.session.query(Book).filter(Book.isbn == isbn).first()
            if check_book:
                raise ValueError("Book with this ISBN already exists")
        book = self.session.query(Book).get(book_id)
        if not book:
            return None
        
        if title: 
            book.title = title
        if author_id:
            book.author_id = author_id
        if published_year:
            book.published_year = published_year
        if isbn:
            book.isbn = isbn

        self.session.add(book)
        self.session.commit()
        self.session.refresh(book)

        return book
    

class StudentService:
    def __init__(self, sessin: Session):
        self.session = sessin

    def create_student(self, full_name: str, email: str, grade: str = None) -> Student:
        """Yangi talaba ro'yxatdan o'tkazish"""
        check_student = self.session.query(Student).filter(Student.email == email).first()
        if check_student:
            raise ValueError("Student email already exists")
        
        student = Student(full_name = full_name, email = email, grade = grade)
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)

        return student

    def get_student_by_id(self, student_id: int) -> Student | None:
        """ID bo'yicha talabani olish"""
        student = self.session.query(Student).get(student_id)
        return student

    def get_all_students(self) -> list[Student]:
        """Barcha talabalar ro'yxatini olish"""
        return self.session.query(Student).all()

    def update_student_grade(self, student_id: int, grade: str) -> Student | None:
        """Talaba sinfini yangilash"""

        student = self.session.query(Student).get(student_id)
        if not student:
            return None

        student.grade = grade
        self.session.add(student)
        self.session.commit()
        self.session.refresh(student)

        return student
    

    def delete_student(self, student_id: int) -> bool:
        """Talabani o'chirish"""
        
        student = self.session.query(Student).get(student_id)
        if not student:
            return False
        
        self.session.delete(student)
        self.session.commit()
        return True
    

class BorrowService:
    def __init__(self, sessin: Session):
        self.session = sessin

    def borrow_book(self, student_id: int, book_id: int) -> Borrow | None:
        """
        Talabaga kitob berish
        """
        student = self.session.query(Student).get(student_id)
        if not student:
            raise ValueError("Student not found")
        book = self.session.query(Book).get(book_id)
        if not book:
            raise ValueError("Book not found")

        if not book.is_available:
            return None

        if len(student.borrows) > 3:
            return None

        borrow = Borrow(student_id=student_id, book_id=book_id)
        self.session.add(borrow)
        book.is_available = False
        self.session.commit()
        self.session.refresh(borrow)

        return borrow
    
    def return_book(self, borrow_id: int) -> bool:
        """
        Kitobni qaytarish
        """
        borrov = self.session.query(Borrow).get(borrow_id)
        if not borrov:  
            return False
        
        book = borrov.book
        if book.is_available:
            return False

        borrov.returned_at = datetime.now()
        self.session.add(borrov)
        book.is_available = True
        self.session.commit()
        return True


class StatisticService:
    def __init__(self, sessin: Session):
        self.session = sessin

    def get_student_borrow_count(self, student_id: int) -> int | None:
        """Talabaning jami olgan kitoblari soni"""
        student = self.session.query(Student).get(student_id)
        if not student:
            return None
        
        borrows = self.session.query(Borrow).filter(Borrow.student_id == student_id).all()
        books = set([borrow.book_id for borrow in borrows])
        return len(books)

    def get_currently_borrowed_books(self) -> list[tuple[Book, Student, datetime]]:
        """Hozirda band bo'lgan kitoblar va ularni olgan talabalar"""
        borrows = self.session.query(Borrow).filter(Borrow.returned_at.is_(None)).all()
        result = []
        for borrow in borrows:
            book = borrow.book
            student = borrow.student
            result.append((book, student, borrow.borrowed_at))
        return result

    def get_books_by_author(self, author_id: int) -> list[Book]:
        """Muayyan muallifning barcha kitoblari"""
        return self.session.query(Book).filter(Book.author_id == author_id).all()
    
    def get_overdue_borrows(self) -> list[tuple[Borrow, Student, Book, int]]:
        """
        Kechikkan kitoblar ro'yxati
        """
        borrows = self.session.query(Borrow).filter(Borrow.returned_at.is_(None)).all()
        result = []
        for borrow in borrows:
            if borrow.due_date < datetime.now():
                result.append((borrow, borrow.student, borrow.book, (datetime.now() - borrow.due_date).days))
        return result