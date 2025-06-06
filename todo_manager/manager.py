from telegram.ext import CommandHandler, ApplicationBuilder
from commands.add import*
from commands.delete import*         
from commands.edit import*
from commands.clean import*
from commands.filter import*
from commands.done_or_not import*
from commands.open_webapp import*
from commands.start import*
from commands.commands import*

BOT_TOKEN="8036426582:AAEkGwTAkzfPKPUn0pCMFV4jAkZKzy6mH34"

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(add_conv_handler)
app.add_handler(del_conv_handler)
app.add_handler(done_conv_handler)
app.add_handler(filter_conv_handler)
app.add_handler(clean_conv_handler)
app.add_handler(edit_conv_handler)

app.add_handler(CommandHandler("view", send_task_list))
app.add_handler(CommandHandler("commands", view_commands))
app.add_handler(CommandHandler("start", start_message))
app.add_handler(CommandHandler("open", open_webapp))  

app.run_polling()
 