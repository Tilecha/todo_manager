import json
import os
from datetime import date
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")    

def load_tasks():

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:

            try:

                return json.load(f)
            
            except json.JSONDecodeError:
                return[]
            
    return []

def save_tasks(memory):
    with open(DATA_PATH, "w") as f:
            json.dump(memory,f)

def is_empty(memory, message="Список пуст."):

    if not memory:
        print(message)
        return True
    
    return False

def done_com(memory):

    if is_empty(memory): return    

    view_com(memory)

    try:

        number = int(input("Какой элемент списка хотите удалить?(Введите 0 для отмены) "))-1

        if 0 <= number < len(memory):
            memory[number]["done"] = not memory[number]["done"]
            save_tasks(memory)
            print("Статус задачи изменён.")

        elif number == -1:
            print("Действие отменено")

        else:
            print("Ошибка: такого элемента нет.")

    except ValueError:
        print("Введите корректное число.")

def filter_by_tag(memory):

    if is_empty(memory): return

    tag = input("Введите тег для поиска: ").strip()

    if not tag:
        print("Тег не должен быть пустым.")
        return

    filtered_tasks = []

    for task in memory:
        if tag in task["tags"]:
            filtered_tasks.append(task)

    if filtered_tasks:
        print(f"Найдено задач с тегом '{tag}':")

        for i, task in enumerate(filtered_tasks, 1):
            status = "✅" if task["done"] else "❌"
            tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
            print(f"{i}. {status} {task['text']} (теги: {tags})")

    else:
        print(f"Задач с тегом '{tag}' не найдено.")

def new_com(memory):

    text = input("Добавьте задачу: ").strip()

    if not text:
        print("Пустую задачу нельзя добавить.")
        return
    
    tags_input = input("Добавьте теги (через запятую, если нужно. Нажмите Enter если не желаете добавлять теги): ").strip()


    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
    new_task = {
        "text": text,
        "done": False,
        "created": date.today().isoformat(),
        "tags": tags
    }
    memory.append(new_task)
    save_tasks(memory)
    print("Задача добавлена.")

def del_com(memory):

    if is_empty(memory): return
    
    view_com(memory)

    try:

        number = int(input("Какой элемент списка хотите удалить?(Введите 0 для отмены) "))-1

        if 0 <= number < len(memory):
            removed = memory.pop(number)
            save_tasks(memory)
            print(f"Удалено: {removed}")

        elif number == -1:
            print("Действие отменено")

        else:
            print("Ошибка: такого элемента нет.")

    except ValueError:
        print("Введите корректное число.")

def edit_com(memory):
    if is_empty(memory): return
    
    view_com(memory)

    try:

        number = int(input("Какой элемент списка хотите редактировать?(Введите 0 для отмены) ")) - 1

        if 0 <= number < len(memory):
            new_text = input("Введите новый текст:").strip()

            if new_text:
                memory[number]["text"] = new_text
                tags_input = input("Введите новые теги (через запятую, если нужно. Нажмите Enter если не желаете добавлять теги): ").strip()
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                memory[number]["tags"] = tags
                save_tasks(memory)
                print("Задача обновлена.")

            else:
                print("Пустую задачу нельзя добавить.")

        elif number == -1:
            print("Действие отменено")

        else:
            print("Ошибка: такого элемента нет.")

    except ValueError:
        print("Введите корректное число.")

def view_com(memory):

    if is_empty(memory): return

    for i, task in enumerate(memory, 1):
        status = "✅" if task["done"] else "❌"
        tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
        print(f"{i}. {status} {task['text']}, теги: {tags})")
        
def del_all_com(memory):

    if is_empty(memory): return

    while True:

        sure = input("Вы уверены? (y/n)").lower().strip()

        if sure == "y":
            memory.clear()
            save_tasks(memory)
            print("список успешно очищен")
            break   

        elif sure == "n":
            print("Удаление отменено.")
            break

        else:
            print("Неверный ввод. Введите 'y' (да) или 'n' (нет).")

memory = load_tasks()

while True:

    try:

        command = int(input(
    "выберите действие: \n"
    "1 - добавить\n"
    "2 - удалить\n"
    "3 - редактировать\n"
    "4 - показать список\n"
    "5 - очистить всё\n"
    "6 - отметить выполненной/не выполненной\n"
    "7 - выйти\n"
    "8 - поиск по тегу\n"
))


        if command == 1:
            new_com(memory)

        elif command == 2:
            del_com(memory)

        elif command == 3:
            edit_com(memory)

        elif command == 4:
            view_com(memory)

        elif command == 5:
            del_all_com(memory)

        elif command == 6:
            done_com(memory)
        elif command == 7:
            break
        elif command == 8:
            filter_by_tag(memory)

    except ValueError:
        print("ошибка, попробуй ещё раз")
        