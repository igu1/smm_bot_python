import requests
import telegram.error
from telegram import *
from telegram.ext import *
from currency_converter import CurrencyConverter
import followers

api_token = '569b161ee684997a5622f133f440ba47d750315b'
url = 'https://.com/api/v1'

package_request = requests.post(url, data={
    'key': api_token,
    'action': 'services'
})

print(package_request.json())