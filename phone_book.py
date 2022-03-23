from tkinter import *
from tkinter import messagebox
from commands import commands


main_color = '#292020' # Основной цвет интерфейса

# Запись номера
def record():
	if len(name_record_entry.get()) > 0 and len(number_record_entry.get()) > 4 and number_record_entry.get().isdigit(): # Если длинна имени > 0, номера > 4 и номер - число
		if commands.CheckNumberInDatabase().execute(number_record_entry.get()): # Проверка на наличие номера в базе, если его нет - номер добавляется
			data = {
			'name' : name_record_entry.get(),
			'phone' : number_record_entry.get()
			}
			commands.AddBookCommands().execute(data)
		else:
			messagebox.showinfo('ОШИБКА', 'Контакт с таким номером уже существует')

		output_to_the_screen()
	else:
		messagebox.showinfo('ЗАПИСЬ КОНТАКТА', 'Чтобы добавить контакт, нужно ввести имя и номер, не короче 4-х цифр')


# Удаляет контакт по номеру
def delete_contact():
	if number_record_entry.get().isdigit():
		commands.DeleteBookCommand().execute(number_record_entry.get())
		messagebox.showinfo('УДАЛЕНИЕ НОМЕРА', 'Контакт был успешно удалён')
	else:
		messagebox.showinfo('ПОДСКАЗКА', 'Чтобы удалить контакт, нужно ввести номер')

	output_to_the_screen()


# Поиск контакта
def search_contact():
	if len(name_record_entry.get()) == 0 and len(number_record_entry.get()) == 0:
		messagebox.showinfo('ПОДСКАЗКА', 'Чтобы найти контакт, нужно ввести имя или номер')
	else:
		data = {}
		if len(name_record_entry.get()) > 0:
			data['name'] = name_record_entry.get()
		if len(number_record_entry.get()) > 0:
			data['phone'] = number_record_entry.get()

		number = formatting(commands.Search().execute(data))

		if len(number) > 0:
			messagebox.showinfo('ПОИСК НОМЕРА', number)
		else:
			messagebox.showinfo('ПОИСК НОМЕРА', 'Номер не найден')


# Форматирование ответа из бд в удобочитаемый вид
def formatting(array):
	s = ''

	for i in range(len(array)):
		s += ' - '.join(array[i]) + '\n'
	return s


# Вывод номеров в текстовое поле
def output_to_the_screen():
	read_field['state'] = 'normal'
	read_field.delete(1.0, END)
	read_field.insert(INSERT, formatting(commands.ListBookCommand().execute()))
	read_field.see(END)
	read_field['state'] = 'disabled'




if __name__ == '__main__':
	commands.CreateBookTableCommand().execute()

	root = Tk()
	root['bg'] = main_color
	# Размеры окна
	WIDTH = 600
	HEIGHT = 800
	# Вычисление середины окна
	POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
	POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
	# Заголовок
	root.title('Телефонная книга')
	#Запрет изменения размера окна
	root.resizable(False, False)
	#Расположение на экране
	root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')

	name_record_lbl = Label(text='Имя',font='Times 20', bg=main_color,fg='white',relief='flat')
	name_record_lbl.place(x=20,y=20)
	number_record_lbl = Label(text='Номер',font='Times 20', bg=main_color,fg='white',relief='flat')
	number_record_lbl.place(x=20,y=110)

	name_record_entry = Entry(font='Times 20', bg='white',fg=main_color,relief='flat')
	name_record_entry.place(x=110,y=20)
	number_record_entry = Entry(font='Times 20', bg='white',fg=main_color,relief='flat')
	number_record_entry.place(x=110,y=110)

	record_bt = Button(text='Записать', font='Times 20', bg=main_color, fg='white', relief='solid', activebackground='#292020', width=35, command = lambda: record())
	record_bt.place(x=30,y=185)
	search_mmbt = Button(text='Найти контакт', font='Times 20', bg=main_color, fg='white', relief='solid', activebackground='#292020', width=35, command = lambda: search_contact())
	search_mmbt.place(x=30,y=235)
	delete_bt = Button(text='Удалить контакт', font='Times 20', bg=main_color, fg='white', relief='solid', activebackground='#292020', width=35, command = lambda: delete_contact())
	delete_bt.place(x=30,y=285)

	read_field = Text(width=54,height=18,font='arial 15')
	read_field.place(x=1,y=375)

	scroll = Scrollbar(command=read_field.yview, width=20)
	scroll.place(x=579,y=376,height=415)
	read_field['yscrollcommand'] = scroll.set

	output_to_the_screen()

	root.mainloop()