import requests
import json

api_token = '$2y$10$k.HNlr2BIl/YQ2o65FyTc.myahj0c3UMMc2JFLcgPxgjkiLyzQlp2'
url = 'https://primesmm.com/api/v2'

package_request = requests.post(url, data={
    'api_token': api_token,
    'action': 'packages'
})


def get_action(data):
    return ['add', data]


def place_order(data):
    r = requests.post(url,
                      data={'api_token':
                                api_token, 'action': 'add',
                            'package': data.get("package"),
                            'link': data.get("link"),
                            'quantity': data.get("quantity")})
    return r.json()


def packages():
    data = package_request.json()
    for x in data:
        x['rate'] = str((float(x["rate"]) + (float(x["rate"]) * 0.75)))[:6]
    return data


def get_services():
    list_services = []
    for x in packages():
        if x['service'] not in list_services:
            list_services.append(x['service'])
    return list_services


def status(id):
    r = requests.post(url,
                      data={'api_token':
                                api_token, 'action': 'status', "order": id})
    return r.json()


def get_real_amount(package):
    data = package_request.json()
    for x in data:
        if (str(x['id'])) == str(package['id']):
            return x['rate']
    return 0
