import requests
from telegram import *
from telegram.ext import *
from currency_converter import CurrencyConverter
import followers

TOKEN = "5536193164:AAEptx2M1C5omh8o8tVPHvqbvA8dgLiNdlU"
updater = Updater(TOKEN,
                  use_context=True)

all_packages = followers.packages()
list_service = followers.get_services()


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hi!!")
    btn = [[
        InlineKeyboardButton(text="Show me services", callback_data="service"),
    ]]
    markup = InlineKeyboardMarkup(btn, resize_keyboard=True)
    update.message.reply_text(
        "Welcome To Hast-la Vista", reply_markup=markup)


def get_item_amount(min_qua, quantity, rate):
    return int(quantity) / int(min_qua * 10) * rate


def order(update: Update, context: CallbackContext):
    if 0 < len(context.args) < 3:
        for x in all_packages:
            if context.args[0] in str(x['id']):
                if int(x['min']) <= int(context.args[1]) <= int(x['max']):
                    c = CurrencyConverter()
                    amount = c.convert(get_item_amount(float(x["min"]), context.args[1], float(x["rate"])), 'USD',
                                       'INR')
                    if float(amount) < 10:
                        amount = 10.00
                    update.message.reply_text(
                        f'Minimum amount your should pay is 10₹\n---------------------------    \nTotal Amount You '
                        f'Should Pay: {str(amount)[:10]}₹',
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="Contact With Admin", url='https://www.instagram.com/direct/t/340282366841710300949128215792275283509' ,callback_data='order_' +
                                                                                                           str(x['id']))]]
                        ))

                else:
                    update.message.reply_text(context.args[1] + " Its Invalid Quantity. Please check you order. "
                                                                "Quantity should be between " + str(x['min']) + " and"
                                                                                                                " " +
                                              str(x['max']))

    else:
        update.message.reply_text('How to order:\n /order {package_id} {quantity}')
        update.message.reply_text('Ex: /order 830 4500\n830 = '
                                  'Package '
                                  'Id\n4500 = No. of followers you want')


# def services(update: Update, context: CallbackContext):
#     btn = []
#     markup = InlineKeyboardMarkup(btn, resize_keyboard=True)
#     for x in range(len(list_service)):
#         btn.append([InlineKeyboardButton(text=f"ID: {x}|{list_service[x]}", callback_data=f"service1_{x}")])
#     message = ''
#     num = 0
#     for x in list_service:
#         message += str(num) + ": " + x
#         message += '\n'
#         num += 1
#     update.message.reply_text("Select the service you want:", reply_markup=markup)


def send_packages(selected_service, chat_id):
    for x in all_packages:
        is_in_list = []
        if selected_service == x['service'] and selected_service not in is_in_list:
            updater.bot.send_message(chat_id=chat_id,
                                     text=f'ID: {str(x["id"])}\nName:{str(x["name"])}\nRate: {str(x["rate"])}\nMin '
                                          f'Quantity: {str(x["min"])}\nMax Quantity: {str(x["max"])}\nService: {str(x["service"])}',
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton("Buy", callback_data=f'buy_{x["id"]}', pay=True),
                                           InlineKeyboardButton("Like🌹",
                                                                callback_data=f'like_{x["id"]}')]])
                                     )
        else:
            is_in_list.append(x['service'])
            pass


def packages(update: Update, context: CallbackContext):
    if len(context.args) != 0:
        update.message.reply_text('Packages:')
        service_type = int(context.args[0])
        selected_service = list_service[service_type]
        update.message.reply_text('Type: ' + selected_service)

        send_packages(selected_service, update.effective_chat.id)
    else:
        update.message.reply_text('''Usage: /packages [service id]''')


def keyboard_callback(update, context):
    query = update.callback_query
    data = update.callback_query.data
    query.answer()
    if 'service1' == str(data).split('_')[0]:
        service_id = str(data).split('_')[1]
        query.answer()
        message_id = query.message.message_id
        updater.bot.edit_message_text(chat_id=query.message.chat.id, message_id=message_id,
                                      text=f"Selected Service: {list_service[int(service_id)]}",
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Show Packages",
                                                                                               callback_data=
                                                                                               "showpackages_" + service_id)]]))
    if 'start_packages' == data:
        print(data)
    if 'service' == str(data).split('_')[0]:
        message_id = query.message.message_id

        btn = [[]]
        markup = InlineKeyboardMarkup(btn, resize_keyboard=True)
        for x in range(len(list_service)):
            btn.append([InlineKeyboardButton(text=f"ID: {x}|{list_service[x]}", callback_data=f"service1_{x}")])
        message = ''
        num = 0
        for x in list_service:
            message += str(num) + ": " + x
            message += '\n'
            num += 1
        updater.bot.send_message(chat_id=query.message.chat.id, text="Select the service you want:",
                                 reply_markup=markup)

    if 'buy' == str(data).split('_')[0]:

        first_name_user = query.message.chat.first_name
        username = query.message.chat.username
        message = query.message.text
        message_id = query.message.message_id
        updater.bot.send_message(chat_id=query.message.chat.id,
                                 text=f'Hey {first_name_user}, \n------------------------------------------\n\nUse:\n'
                                                                     f'    /order {str(data).split("_")[1]} [quantity'
                                                                     f']\n\n------------------------------------------')
    if 'like' == str(data).split('_')[0]:
        print(data)
    if 'order' == str(data).split('_')[0]:
        pass
    if 'showpackages' == str(data).split('_')[0]:
        chat_id = query.message.chat.id
        send_packages(list_service[int(str(data).split('_')[1])], chat_id)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('packages', packages))
# updater.dispatcher.add_handler(CommandHandler('service', services))
updater.dispatcher.add_handler(CommandHandler('order', order))

updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callback))

updater.start_polling()
