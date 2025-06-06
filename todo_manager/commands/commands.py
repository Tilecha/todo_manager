from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes

async def view_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/add - добавить\n /del - удалить\n /view - посмотреть список\n /clean - очистить список\n /cancel - отменить действие\n /edit - отредактировать\n /filter - искать по тегам\n /done - отметить выполненой")
    return ConversationHandler.END
