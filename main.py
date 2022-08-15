from flask import Flask
from flask import request
from flask import Response
import requests
from followers import packages

TOKEN = "5536193164:AAEptx2M1C5omh8o8tVPHvqbvA8dgLiNdlU"
app = Flask(__name__)


def parse_message(message):
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        username, first_name = message['message']['chat']['username'], message['message']['chat']['first_name']
        return username, first_name, chat_id, txt
    except KeyError:
        print('error found')
        return 'check', 'eza', '0000', 'hello'


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        username, firstname, chat_id, txt = parse_message(msg)
        if txt == "/start":
            tel_send_message(chat_id, 'Hi!... I am cheap followers seller')
            tel_send_message(chat_id, "Disclaimer: Non refill pack won't refill your followers")
            tel_send_message(chat_id,'''
                Commands:
                1./packages {TYPE}
                2./status
                3./order
            ''')
        elif "/packages" in txt:
            try:
                message, service_type = str(txt).lower().split(' ')
                tel_send_message(chat_id, f'{str(service_type)} services:')
                for x in packages():
                    if str(service_type).lower() in x.lower():
                        tel_send_message(chat_id, x + '\n')
            except ValueError:
                tel_send_message(chat_id,
                                 '''Use Command: /packages {type}
                                     Ex:/packages instagram
                                          /packages youtube
                                          /packages discord''')
        else:
            tel_send_message(chat_id, 'Sorry... i think its an invalid command!😢')
        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
