import json
import uuid
import os


class Book:
    def __init__(self, title, author, year, book_id=None, status="в наличии"):
        self.id = book_id if book_id else str(uuid.uuid4())[:5]
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return '{0:^10}|{1:^25}|{2:^25}|{3:^14}|{4:^14}'.format(self.id, self.title, self.author, self.year, self.status) + '\n' + '-' * 90
        #return f"ID: {self.id}, Название: {self.title}, Автор: {self.author}, Год издания: {self.year}, Статус: {self.status}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['title'], data['author'], data['year'], data['id'], data['status'])


class Library:
    def __init__(self, db_path="library.json"):
        self.db_path = db_path
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book.from_dict(book) for book in data]
        return []

    def save_books(self):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book = Book(title, author, year)
        self.books.append(book)
        self.save_books()
        print("Книга добавлена!")

    def delete_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print("Книга удалена!")
                return
        print("Книга с указанным ID не найдена.")

    def find_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                print(book)
                return
        print("Книга с указанным ID не найдена.")

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.")
        else:
            print('{0:^10}|{1:^25}|{2:^25}|{3:^14}|{4:^14}'.format('ID', 'Название', 'Автор', 'Год издания', 'Статус') + '\n' + '-' * 90)
            for book in self.books:
                print(book)

    def change_status(self, book_id, status):
        for book in self.books:
            if book.id == book_id:
                if status in ["в наличии", "выдана"]:
                    book.status = status
                    self.save_books()
                    print("Статус книги обновлен!")
                else:
                    print("Неверный статус.")
                return
        print("Книга с указанным ID не найдена.")


def main():
    library = Library()

    while True:
        print("\n1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите опцию: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            library.delete_book(book_id)
        elif choice == "3":
            book_id = input("Введите ID книги для поиска: ")
            library.find_book(book_id)
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            status = input("Введите новый статус (в наличии/выдана): ")
            library.change_status(book_id, status)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
