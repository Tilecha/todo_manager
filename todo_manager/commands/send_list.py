from telegram.ext import ContextTypes
from telegram import Update
from commands.load import load_tasks

async def send_task_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    tasks = load_tasks()
    
    if not tasks: 
        await update.message.reply_text("Список задач пуст.")
        return False

    response = ""

    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "❌"
        tags = ", ".join(task["tags"]) if task["tags"] else "Без тегов"
        response += f"{i}. {status} {task['text']}, теги: {tags}\n"

    await update.message.reply_text(response)
    return True
