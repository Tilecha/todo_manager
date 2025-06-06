from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from datetime import date
from commands import cancel
from commands.load import load_tasks
from commands.save import save_tasks

ASK_TASK = 1
ASK_TAGS = 2


async def add_receive_tags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tags_text = update.message.text.strip()
    tags = []

    if tags_text != '/skip':
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

    await update.message.reply_text(
    "Задача добавлена ✅\n\n📝 Текст: {}\n🏷️ Теги: {}".format(
        new_task["text"],
        ", ".join(tags) if tags else "нет"
    )
)

    context.user_data.clear()
    return ConversationHandler.END

async def add_receive_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = update.message.text.strip()

    if not task_text:
        await update.message.reply_text("Задача не может быть пустой. Пожалуйста, введите текст задачи.")
        return ASK_TASK
    
    context.user_data["task_text"] = task_text
    await update.message.reply_text("Добавь теги через запятую (/skip для пропуска)")
    return ASK_TAGS

async def add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши задачу")
    return ASK_TASK

add_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("add", add_start)],
    states={
        ASK_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_receive_task)],
        ASK_TAGS: [MessageHandler(filters.TEXT, add_receive_tags)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)