from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from commands.cancel import cancel
from commands.load import load_tasks
from commands.save import save_tasks
from commands.send_list import send_task_list

DELETE_STATE = 3

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

async def del_task(update: Update,context: ContextTypes.DEFAULT_TYPE):
    success = await send_task_list(update,context)
    if not success:
        return ConversationHandler.END

    await update.message.reply_text("Напиши номер задачи для удаления")
    return DELETE_STATE

del_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("del", del_task)],
    states={
        DELETE_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, del_receive_number)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
