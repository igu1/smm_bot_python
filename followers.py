import requests
import json

api_token = '$2y$10$k.HNlr2BIl/YQ2o65FyTc.myahj0c3UMMc2JFLcgPxgjkiLyzQlp2'
url = 'https://primesmm.com/api/v2'


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
    r = requests.post(url, data={
        'api_token': api_token,
        'action': 'packages'
    })
    data = r.json()
    return data


def status(id):
    r = requests.post(url,
                      data={'api_token':
                                api_token, 'action': 'status', "order": id})
    return r.json()
