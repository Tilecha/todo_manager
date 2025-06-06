from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from commands.cancel import cancel
from commands.load import load_tasks

FILTER_BY_TAG_STATE = 7

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


async def filter_by_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks: 
        await update.message.reply_text("Список пуст.")
        return ConversationHandler.END
    await update.message.reply_text('Введите теги для поиска')
    return FILTER_BY_TAG_STATE


filter_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("filter", filter_by_tag)],
    states={
        FILTER_BY_TAG_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, filter_by_tag_receive_task)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
