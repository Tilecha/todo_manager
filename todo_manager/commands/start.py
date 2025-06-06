from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes

async def start_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "Привет! 👋 Я твой трекер задач.\n"
    "Напиши /commands чтобы увидеть что умеет этот бот"
)
    return ConversationHandler.END
