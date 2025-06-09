from telegram import Update
from telegram.ext import ContextTypes
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup

async def open_webapp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Открыть трекер", web_app=WebAppInfo(url="https://todo-manager-n3vu.onrender.com"))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Нажми кнопку ниже, чтобы открыть мини-приложение", reply_markup=reply_markup)
