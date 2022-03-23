import sys

from database.database import DatabaseManager

db = DatabaseManager('phone_book.db')

# Создание таблицы
class CreateBookTableCommand:
	def execute(self):
		db.create_table('phone_book', {
			'name' : 'text not null',
			'phone' : 'text not null'
			})


# Добавление контакта
class AddBookCommands:
	def execute(self, data):
		db.add('phone_book', data)

# Удаление контакта
class DeleteBookCommand:
	def execute(self, data):
		db.delete('phone_book', {'phone' : data})


# Вывод контактов (сортировка по имени)
class ListBookCommand:
	def __init__(self, order_by = 'name'):
		self.order_by = order_by

	def execute(self):
		return db.select('phone_book', order_by = self.order_by).fetchall()


# Проверка: есть ли контакт в базе
class CheckNumberInDatabase:
	def execute(self, data):
		return db.check('phone_book', {'phone' : data})


# Поиск контакта
class Search:
	def execute(self, data):
		return db.search('phone_book', data).fetchall()