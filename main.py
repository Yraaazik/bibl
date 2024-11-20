import json
import os

class Book: #класс книг
    def __init__(self, book_id, title, author, year, status="в наличии"):#сохранение переменных класса
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):#сохранение в формате json
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }
class Library: #класс библиотек
    def __init__(self, filename='library.json'):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):#загрузка всех книг
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.books = [Book(**book) for book in json.load(f)]

    def save_books(self):#сохранение книги в json
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):#добавить книгу
        new_id = 1 if not self.books else max(book.id for book in self.books) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id):#удалить книгу
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def search_books(self, search_term): #поиск книг
        results = [book for book in self.books if search_term.lower() in book.title.lower() or
                   search_term.lower() in book.author.lower() or
                   search_term == str(book.year)]
        return results

    def display_books(self):#отображение книг в print
        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"ID: {book.id}, Название: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: '{book.status}'")

    def update_status(self, book_id, new_status): #обновление статуса книг
        book_to_update = next((book for book in self.books if book.id == book_id), None)
        if book_to_update:
            if new_status in ["в наличии", "выдана"]:
                book_to_update.status = new_status
                self.save_books()
            else:
                print("Неверный статус. Доступные статусы: 'в наличии', 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nДоступные команды:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите команду: ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)

        elif choice == '2':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == '3':
            search_term = input("Введите название, автора или год для поиска: ")
            results = library.search_books(search_term)
            if results:
                for book in results:
                    print(f"Найдена книга - ID: {book.id}, Заголовок: '{book.title}', Автор: '{book.author}', Год: {book.year}, Статус: '{book.status}'")
            else:
                print("Книги не найдены.")

        elif choice == '4':
            library.display_books()

        elif choice == '5':
            book_id = int(input("Введите ID книги для изменения статуса: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, new_status)

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите правильный номер команды.")

if __name__ == "__main__":
    main()