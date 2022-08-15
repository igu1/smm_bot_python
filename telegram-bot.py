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
    /packages - usage: /package {service-id}
    /services - to get service_id
    /order - To get the GeeksforGeeks URL""")


def get_services():
    list_service = []
    for x in followers.packages():
        if x['service'] not in list_service:
            list_service.append(x['service'])
    return list_service


def services(update: Update, context: CallbackContext):
    list_service = get_services()
    message = ''
    num = 0
    for x in list_service:
        message += str(num) + ": " + x
        message += '\n'
        num += 1
    update.message.reply_text(message)


def packages(update: Update, context: CallbackContext):
    update.message.reply_text('Packages:')
    service_type = int(context.args[0])
    selected_service = get_services()[service_type]
    all_packages = followers.packages()

    update.message.reply_text('Type: ' + selected_service)
    for x in all_packages:
        is_in_list = []
        if selected_service == x['service'] and selected_service not in is_in_list:
            update.message.reply_text(
                f'ID: {str(x["id"])}\nName:{str(x["name"])}\nRate: {str(float(x["rate"]) + float(x["rate"]) * 0.25)[:6]}\nMin '
                f'Quantity: {str(x["min"])}\nMax Quantity: {str(x["max"])}\nService: {str(x["service"])}')
        else:
            is_in_list.append(x['service'])
            pass


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('packages', packages))
updater.dispatcher.add_handler(CommandHandler('services', services))

updater.start_polling()
