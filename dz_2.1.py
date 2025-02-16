class Book:  # Класс книги
    def __init__(self,
                 title: str,
                 author: str,
                 year: int,
                 isbn: int):
        self.title = title
        self.author = author
        self.year = year
        self.isbn = isbn

    def __str__(self):
        return f"Название: {self.title}, Автор: {self.author}, Год: {self.year}, ISBN: {self.isbn}"


class Library: # Класс библиотеки
    def __init__(self):
        self.books = []  #Инициализируем пустой список

        # Добавление книги в библиотеку
    def add_book(self, book):
        if isinstance(book, Book):
            self.books.append(book)
            print(f"Книга '{book.title}' успешно добавлена в библиотеку")

        # Удаление книги из библиотеку по ISBN
    def remove_book(self, isbn: int):
        flag_book = False
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                flag_book = True
                print(f'Книга с номером ISBN: {isbn} успешно удаленна')
        if flag_book == False:
            print(f'Книга с номером ISBN: {isbn} не найдена')

    # Поиск книги библиотеке по названию
    def find_book_by_title(self, title):
        flag_book = False
        for book in self.books:
            if book.title == title:
                print(f"Найдена книга с названием {title}"
                      f", автором: {book.author},"
                      f" годом: {book.year} и"
                      f" ISBN: {book.isbn}")
                flag_book = True

        if flag_book == False:
            print(f"Извините, но книги {title} нету в библиотеке")

    # Выведение всех книг из библиотеки
    def list_books(self):
        if self.books == []:
            print("Библиотека пуста")
        print("Список книг в библиотеке:")
        for book in self.books:
            print(f"{book}")


library = Library()

book1 = Book('Mah', 'mars', 1933, 734547)
book2 = Book('Mahg', 'marsel', 1945, 735677)


library.add_book(book1)
library.add_book(book2)
library.list_books()
library.find_book_by_title('Mah')
library.find_book_by_title('Mahddddd')  # Для проверки если такой книги нету
library.remove_book(734547)
library.remove_book(734549)  # Для проверки если такой ISBN нету
library.list_books()
