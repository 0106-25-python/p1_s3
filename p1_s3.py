import uuid
from datetime import datetime
import sys

# Константы
STATUS_ACTIVE = "active"
STATUS_DONE = "done"
SEPARATOR = "<>" 
DB_FILE_PATH = "db.txt"

NEW_TASK_ITEM = "1"
COMPLETE_TASK_ITEM = "2"
CHANGE_TASK_ITEM = "3"
SHOW_COMPLETED_TASKS = "4"
ERASE_COMPLETED_TASKS = "5"
EXIT_ITEM = "0"
MENU_ITEMS = {
	NEW_TASK_ITEM: "Создать новую задачу",
	COMPLETE_TASK_ITEM: "Завершить задачу",
	CHANGE_TASK_ITEM: "Изменить параметры задачи",
    SHOW_COMPLETED_TASKS: "Показать завершённые задачи",
    ERASE_COMPLETED_TASKS: "Очистить все завершённые задачи",
	EXIT_ITEM: "Выйти из программы"
}

#----------#
# Блок функций для чтения/записи в файл
#----------#
# Читаем ВСЕ содержимое файла
def read_from_db():
	file_object = open(DB_FILE_PATH, "r", encoding="utf8")
	file_content = file_object.read()
	file_object.close()
	return file_content


# Добавляем новую строку в файл
def append_new_line_to_db(new_line): 
	file_object = open(DB_FILE_PATH, "a", encoding="utf8")
	file_object.write("\n") 
	file_object.write(new_line)
	file_object.close()


# Перезаписываем все задачи
def rewrite_db(raw_content): 
	file_object = open(DB_FILE_PATH, "w", encoding="utf8")
	file_object.write(raw_content)
	file_object.close()	


#----------#
# Преобразуем содержимое файла в список задач
def deserialize_tasks_from_db(raw_content):
	raw_tasks = raw_content.splitlines()
	tasks = []
	for task_info in raw_tasks:
		splitted_task = task_info.split(SEPARATOR) 
		tasks.append(splitted_task)
	return tasks


# Подготавливаем список задач для вывода в консоль
def prepare_tasks_list_to_output(raw_tasks_list):
    tasks = []
    for task_info in raw_tasks_list:
        status = "✓" if task_info[4] == STATUS_ACTIVE else "✕"
        task = status + " " + task_info[1] + " " + task_info[2] + " " + task_info[3] # склеиваем параметры задачи
        tasks.append(task)
    return tasks


# Превращаем информацию о задаче в строку для последующего сохранения в БД
def serialize_task_for_db(task_data):
	return SEPARATOR.join([task_data[0], task_data[1], task_data[2], task_data[3], task_data[4]])
	

# Подготавливаем новую задачу для сохранения
def prepare_new_task_to_save(task_info): 
	task_id = uuid.uuid4() 
	task_date_created = datetime.now() 
	task_to_save = serialize_task_for_db([str(task_id), task_info[0], "["+task_info[1]+"]", str(task_date_created), STATUS_ACTIVE])
	return task_to_save


# Получаем список всех задач из БД и подготавливаем к выводу в консоль
def get_all_tasks():
    # ТУДУ: Реализовать логику отображения только активных задач
    all_tasks = read_from_db()
    raw_tasks = deserialize_tasks_from_db(all_tasks)
    tasks_list_to_print = prepare_tasks_list_to_output(raw_tasks)
    return tasks_list_to_print


# Парсим введённые пользователем параметры задачи: описание и дату исполнения
def parse_new_task_input(raw_data):
	splitted_params = raw_data.split("[") 
	task_description = splitted_params[0].strip()
	task_due_date = ""

	if len(splitted_params) == 2:
		task_due_date = splitted_params[1].replace("]","")

	return [task_description, task_due_date]


#----------#

# Действие меню "Новая задача"
def action_new_task():
    print("#------------------#")
    print("Введите параметры новой задачи или 0, чтобы вернуться в предыдущее меню:")
    new_task_info = input()
    
    if new_task_info == "0": return

    task_data = parse_new_task_input(new_task_info)
    task_to_save = prepare_new_task_to_save(task_data)
    append_new_line_to_db(task_to_save)


# Действие меню "Завершить задачу"
def action_complete_task():
	print("#------------------#")
	print("Введите номер задачи для завершения или 0, чтобы вернуться в предыдущее меню")
    #ТУДУ: Реализовать логику завершения задачи, т.е. изменения статуса с active на done


# Действие меню "Изменить параметры задачи"
def action_change_task_params():
	print("#------------------#")
	print("Введите номер задачи для изменения её параметров или 0, чтобы вернуться в предыдущее меню")    
    #ТУДУ: Реализовать логику изменения параметров задачи, т.е. изменения описания и/или времени исполнения

# Действие меню "Показать завершённые задачи"
def show_completed_tasks():
    print("#------------------#")
    print("Завершённые задачи:")
    #ТУДУ: Реализовать логику отображения всех завершённых задач

# Действие меню "Очистить все завершённые задачи"
def erase_completed_tasks():
    print("#------------------#")
    print("Очищаем базу от завершённых задач...")
    #ТУДУ: Реализовать логику очистки БД от завершенных задач    

#----------#
# Вывод в консоль
#----------#
# Вывод списка задач в консоль
def print_all_tasks_to_console(tasks):
	counter = 1
	print("Актуальные задачи:")
	for task_info in tasks:
		print(str(counter) + ": " + task_info)
		counter += 1


# Вывод основного меню
def show_main_menu():
    print("#------------------#")
    print("Выберите действие:")
    menu_text = ""
    for key, value in MENU_ITEMS.items():
        menu_text = menu_text + key + " – " + value + "\n"
    
    print(menu_text)
    print("Номер действия: ")
    choice = input()
    
    if choice == NEW_TASK_ITEM:
        action_new_task()
    elif choice == COMPLETE_TASK_ITEM:
        action_complete_task()
    elif choice == CHANGE_TASK_ITEM:
        action_change_task_params()
    elif choice == EXIT_ITEM:
        sys.exit()
    else:
        print("Неизвестная команда")


# Основная функция с постоянным выводом списка задач и меню
def main():
	while True:
		tasks_list = get_all_tasks()
		print_all_tasks_to_console(tasks_list)

		show_main_menu()


# Вызов основной функции при запуске
main()