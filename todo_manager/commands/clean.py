from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from commands.cancel import cancel
from commands.load import load_tasks
from commands.save import save_tasks


CLEAN_CONFIRM = 6

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

async def clean_start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks: 
        await update.message.reply_text("Список и так пуст.")
        return ConversationHandler.END
    await update.message.reply_text("Вы уверены? да/нет")
    return CLEAN_CONFIRM

clean_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("clean", clean_start)],
    states={
        CLEAN_CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, clean_confirm)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
