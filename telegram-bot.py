from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import followers

TOKEN = "5536193164:AAEptx2M1C5omh8o8tVPHvqbvA8dgLiNdlU"

updater = Updater(TOKEN,
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi!!")
    update.message.reply_text(
        "Welcome To Hast-la Vista")
    update.message.reply_text("""Available Commands :-
    /start - To get the youtube URL
    /packages - To get the LinkedIn profile URL
    /status - To get gmail URL
    /order - To get the GeeksforGeeks URL""")


def services(update: Update, context: CallbackContext):
    list_service = []
    for x in followers.packages():
        if x['service'] not in list_service:
            list_service.append(x['service'])
    message = ''
    for x in list_service:
        if x not in 'likee.com':
            message += x
            message += '\n'
    update.message.reply_text(message)


def packages(update: Update, context: CallbackContext):
    update.message.reply_text('Packages:')
    service_type = context.args[0]
    update.message.reply_text('Type: ' + service_type)
    for x in followers.packages():
        if service_type == str(x['service']).lower():
            update.message.reply_text(
                f'ID: {str(x["id"])}\nName:{str(x["name"])}\nRate: {str(x["rate"])}\nMin Quantity: {str(x["min"])}\nMax Quantity: {str(x["max"])}\nService: {str(x["service"])}')


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('packages', packages))
updater.dispatcher.add_handler(CommandHandler('service', services))


updater.start_polling()
