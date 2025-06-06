from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from commands.cancel import cancel
from commands.load import load_tasks
from commands.save import save_tasks
from commands.send_list import send_task_list

DONE_OR_NOT_STATE = 8

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
    if not tasks: 
        await update.message.reply_text("Список пуст.")
        return ConversationHandler.END
    success = await send_task_list(update, context)
    await update.message.reply_text('Напишите номер задачи')
    return DONE_OR_NOT_STATE

done_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("done", done_or_not)],
    states={
        DONE_OR_NOT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, done_or_not_receive_task)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
