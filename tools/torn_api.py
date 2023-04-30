import requests

from config import TORN_API_KEY


class TornApi:
    def __init__(self, key=TORN_API_KEY):
        self.key = key
        self.api_type = ''
        self.query_id = ''
        self.Selections = ''
        self.url = ''

    def get_info(self, api_type, selections, query_id=''):
        self.api_type = api_type
        self.query_id = query_id
        self.Selections = selections
        self.url = f'https://api.torn.com/{self.api_type}/{self.query_id}?selections={self.Selections}&key={self.key}'
        print(f'开始请求：{self.url}')
        try:
            data = requests.get(self.url).json()
        except Exception as e:
            print('error--:', e)
            return e
        return data
