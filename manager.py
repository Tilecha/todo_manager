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

def new_com(memory):

    text = input("Добавьте задачу: ").strip()

    if not text:
        print("Пустую задачу нельзя добавить.")
        return
    
    tags_input = input("Добавьте теги (через запятую, если нужно. Нажмите Enter если не желаете добавлять теги): ").strip()

    if tags_input:
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

    elif not tags_input:
        new_task = {
            "text": text,
            "done": False,
            "created": date.today().isoformat(),
            "tags": "Отсутствует"
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
            new_text = input("Введите текст:").strip()

            if new_text:
                memory[number]=new_text
                save_tasks(memory)

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
        print(f"{i}. {task}")

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

        command = int(input("выберите действие: (1 - добавить, 2 - удалить, 3 - редактировать, 4 - список, 5 - очистить всё, 6 - выйти)"))

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
            break

    except ValueError:
        print("ошибка, попробуй ещё раз")
        