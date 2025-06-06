from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from commands.add import add_receive_tags
from commands.cancel import cancel
from commands.load import load_tasks
from commands.save import save_tasks
from commands.send_list import send_task_list

ASK_TASK = 1
ASK_TAGS = 2
EDIT_STATE = 4
EDIT_TAGS = 5


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

edit_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("edit", edit_task)],
    states={
        EDIT_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_receive_task)],
        ASK_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_receive_new_text)],
        EDIT_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_tags)],
        ASK_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_receive_tags)],  
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

