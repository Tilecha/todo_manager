from telegram.ext import CommandHandler, ApplicationBuilder
from commands.data import*
from telegram.ext import MessageHandler, filters
from commands.data import handle_webapp_data

BOT_TOKEN="8036426582:AAEkGwTAkzfPKPUn0pCMFV4jAkZKzy6mH34"

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
app.run_polling()
 