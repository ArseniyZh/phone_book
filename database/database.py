from datetime import datetime
import sqlite3


class DatabaseManager:
	def __init__(self, database_filename):
		self.connection = sqlite3.connect(database_filename)

	def __del__(self):
		self.connection.close()

	# Выполняет все действия с БД
	def _execute(self, statement, values = None):
		with self.connection:
			cursor = self.connection.cursor()
			cursor.execute(statement, values or []) # Задаёт курсору параметры
			return cursor

	# Создание таблицы в БД
	def create_table(self, table_name, columns):
		columns_with_types = [f'{column_name} {data_type}' for column_name, data_type in columns.items()] # Задаёт список с названием таблицы и колонками с их типами
		self._execute(
			f'''
			CREATE TABLE IF NOT EXISTS {table_name}
			({', '.join(columns_with_types)});
			'''
			)

	# Добавляет запись в таблицу
	def add(self, table_name, data):
		placeholders = ', '.join('?' * len(data)) # Задаёт плейсхолдеры (по синтаксису MySQLite) от SQL иньекции - '?, ?, ? ...'
		column_names = ', '.join(data.keys()) # Задаёт названия колонок
		column_values = tuple(data.values()) # Задаёт значения колонок

		self._execute(
			f'''
			INSERT INTO {table_name}
			({column_names})
			VALUES ({placeholders});
			''',
			column_values
			)

	# Удаляет запись из таблицы
	def delete(self, table_name, criteria):
		placeholders = [f'{column} = ?' for column in criteria.keys()] # Задаёт плейсхолдеры формата column = ?
		delete_criteria = ' AND '.join(placeholders) # Удаляет запись по указанным критериям
		self._execute(
			f'''
			DELETE FROM {table_name}
			WHERE {delete_criteria};
			''',
			tuple(criteria.values())
			)


	# Выбирает запись курсором
	def select(self, table_name, order_by = None, criteria = None):
		criteria = criteria or {}

		query = f'SELECT * FROM {table_name}'

		# Выбирает запись по указанным параметрам
		if criteria:
			placeholders = [f'{column} = ?' for column in criteria.keys()]
			select_criteria = ' AND '.join(placeholders)
			query += f' WHERE {select_criteria}'

		# Критерии для сортировки записей
		if order_by:
			query += f' ORDER BY {order_by}'

		return self._execute(
			query,
			tuple(criteria.values())
			)

	# Проверяет номер на наличие в базе
	def check(self, table_name, criteria):
		placeholders = [f'{column} = ?' for column in criteria.keys()] # Задаёт плейсхолдеры формата column = ?
		check_criteria = ' AND '.join(placeholders)

		check = f'''
		SELECT * FROM {table_name}
		WHERE {check_criteria}
		'''

		return self._execute(check, tuple(criteria.values())).fetchall() == []


	# Поиск контакта
	def search(self, table_name, criteria):
		placeholders = [f'{column} = ?' for column in criteria.keys()] # Задаёт плейсхолдеры формата column = ?
		search_criteria = ' AND '.join(placeholders)

		search = f'''
		SELECT * FROM {table_name}
		WHERE {search_criteria}
		'''

		return self._execute(search, tuple(criteria.values()))