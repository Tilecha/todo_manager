from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes, ApplicationBuilder
import json
import os
from datetime import date
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")    

ASK_TASK = 1
ASK_TAGS = 2
DELETE_STATE = 3
EDIT_STATE = 4
CLEAN_CONFIRM = 5
EDIT_TAGS = 6
FILTER_BY_TAG_STATE = 7
DONE_OR_NOT_STATE = 8

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
            json.dump(memory,f,ensure_ascii=False, indent=2)

def is_empty(memory):
    if not memory:
        return True
    
    return False



async def add_receive_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = update.message.text.strip()

    if not task_text:
        await update.message.reply_text("Задача не может быть пустой. Пожалуйста, введите текст задачи.")
        return ASK_TASK
    
    context.user_data["task_text"] = task_text
    await update.message.reply_text("Добавь теги через запятую (/none для пропуска)")
    return ASK_TAGS

async def add_receive_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tags_text = update.message.text.strip()
    tags = []

    if tags_text != '/none':
        tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]

    task_text = context.user_data.get("task_text", "Без названия")

    tasks = load_tasks()

    new_task = {
        "text": task_text,
        "done": False,
        "created": date.today().isoformat(),
        "tags": tags
    }

    tasks.append(new_task)
    save_tasks(tasks)

    await update.message.reply_text(f"Задача добавлена: {new_task['text']} с тегами: {', '.join(tags) if tags else 'нет'}")
    context.user_data.clear()
    return ConversationHandler.END

async def del_receive_number(update: Update,context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Пожалуйста, введи номер задачи числом.")
        return DELETE_STATE
    
    task_index = int(text)-1

    if task_index < 0 or task_index >= len(tasks):
        await update.message.reply_text("Неверный номер задачи. Попробуй снова.")
        return DELETE_STATE
    
    removed_task = tasks.pop(task_index)
    save_tasks(tasks)

    await update.message.reply_text(f"Задача удалена: {removed_task['text']}")

    return ConversationHandler.END

async def clean_confirm(update:Update,context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if text == "да":
        save_tasks([])
        await update.message.reply_text("Список очищен.")
        return ConversationHandler.END
    elif text == 'нет':
        await update.message.reply_text("Очистка отменена.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, напишите 'да' или 'нет'.")
        return CLEAN_CONFIRM

async def edit_receive_task(update:Update,context:ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Пожалуйста, введи номер задачи числом.")
        return EDIT_STATE
    
    task_index = int(text)-1
    if task_index < 0 or task_index >= len(tasks):
        await update.message.reply_text("Неверный номер задачи. Попробуй снова.")
        return EDIT_STATE
    task = tasks[task_index]
    tags = task["tags"]

    

    context.user_data["edit_index"] = task_index
    await update.message.reply_text("Введите новую задачу:")
    return ASK_TASK

async def edit_receive_new_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    task_index = context.user_data["edit_index"]
    new_text = update.message.text.strip()

    tasks[task_index]["text"] = new_text
    save_tasks(tasks)

    await update.message.reply_text(f"Задача обновлена: {new_text}")
    await update.message.reply_text("Хотите изменить теги? (да/нет)")
    return EDIT_TAGS

async def filter_by_tag_receive_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    tag = update.message.text.strip().lower()
    matched_tasks = []
    for i, task in enumerate(tasks, 1):
        for t in task.get("tags", []):
            if t.lower() == tag:
                matched_tasks.append((i,task))
                break
    if not matched_tasks:
        await update.message.reply_text(f"Задач с тегом '{tag}' не найдено.")
    else:
        response = f"Задачи с тегом '{tag}':\n"
        for i, task in matched_tasks:
            status = "✅" if task["done"] else "❌"
            tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
            response += f"{i}. {status} {task['text']}, теги: {tags}\n"
        await update.message.reply_text(response)

    return ConversationHandler.END

async def done_or_not_receive_task(update:Update,context:ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Пожалуйста, введи номер задачи числом.")
        return DONE_OR_NOT_STATE
    
    task_index = int(text)-1
    if task_index < 0 or task_index >= len(tasks):
        await update.message.reply_text("Неверный номер задачи. Попробуй снова.")
        return DONE_OR_NOT_STATE
    tasks[task_index]["done"]=not tasks[task_index]["done"]
    save_tasks(tasks)

    status = "✅ Выполнено" if tasks[task_index]["done"] else "❌ Не выполнено"
    await update.message.reply_text(f"Статус задачи изменён: {status} — {tasks[task_index]['text']}")
    
    return ConversationHandler.END 





async def done_or_not(update: Update,context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if is_empty(tasks):
        await update.message.reply_text("Список пуст.")
        return ConversationHandler.END
    success = await send_task_list(update, context)
    await update.message.reply_text('Напишите номер задачи')
    return DONE_OR_NOT_STATE

async def filter_by_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if is_empty(tasks):
        await update.message.reply_text("Список пуст.")
        return ConversationHandler.END
    await update.message.reply_text('Введите теги для поиска')
    return FILTER_BY_TAG_STATE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Действие отменено.")
    return ConversationHandler.END

async def send_task_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    tasks = load_tasks()
    
    if is_empty(tasks): 
        await update.message.reply_text("Список задач пуст.")
        return False

    response = ""

    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "❌"
        tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
        response += f"{i}. {status} {task['text']}, теги: {tags}\n"

    await update.message.reply_text(response)
    return True

async def del_task(update: Update,context: ContextTypes.DEFAULT_TYPE):
    success = await send_task_list(update,context)
    if not success:
        return ConversationHandler.END

    await update.message.reply_text("Напиши номер задачи для удаления")
    return DELETE_STATE

async def clean_start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if is_empty(tasks):
        await update.message.reply_text("Список и так пуст.")
        return ConversationHandler.END
    await update.message.reply_text("Вы уверены? да/нет")
    return CLEAN_CONFIRM

async def edit_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    success = await send_task_list(update, context)
    if not success:
        return ConversationHandler.END

    await update.message.reply_text("Напишите номер задачи для редактирования")
    return EDIT_STATE

async def edit_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.strip().lower()
    if answer == "да":
        await update.message.reply_text("Введите новые теги через запятую:")
        return ASK_TAGS
    elif answer == "нет":
        await update.message.reply_text("Редактирование завершено.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Пожалуйста, напишите 'да' или 'нет'.")
        return EDIT_TAGS

async def view_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/add - добавить\n /del - удалить\n /view - посмотреть список\n /clean - очистить список\n /cancel - отменить действие\n /edit - отредактировать\n /filter - искать по тегам\n /done - отметить выполненой")
    return ConversationHandler.END

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши задачу")
    return ASK_TASK

async def start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "Привет! 👋 Я твой трекер задач.\n"
    "Напиши /commands чтобы увидеть что умеет этот бот"
)
    return ConversationHandler.END

add_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_start)],
    states={
        ASK_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_receive_task)],
        ASK_TAGS: [MessageHandler(filters.TEXT, add_receive_tags)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

done_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("done", done_or_not)],
    states={
        DONE_OR_NOT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, done_or_not_receive_task)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

del_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("del", del_task)],
    states={
        DELETE_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_receive_number)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

clean_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("clean", clean_start)],
    states={
        CLEAN_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, clean_confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

edit_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("edit", edit_task)],
    states={
        EDIT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_receive_task)],
        ASK_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_receive_new_text)],
        EDIT_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_tags)],
        ASK_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_receive_tags)],  # переиспользуем
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

filter_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("filter", filter_by_tag)],
    states={
        FILTER_BY_TAG_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, filter_by_tag_receive_task)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app = ApplicationBuilder().token("YOUR TOKEN").build()

app.add_handler(add_conv_handler)

app.add_handler(del_conv_handler)

app.add_handler(done_conv_handler)

app.add_handler(filter_conv_handler)

app.add_handler(clean_conv_handler)

app.add_handler(edit_conv_handler)

app.add_handler(CommandHandler("view", send_task_list))

app.add_handler(CommandHandler("commands", view_commands))

app.add_handler(CommandHandler("start", start_message))

app.run_polling()
