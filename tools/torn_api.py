import requests
from fastapi import status

from config import TORN_API_KEY, IS_TESTING_SERVICE

ERROR_DESCRIPTION = {
    0: "Unknown error : Unhandled error, should not occur.",
    1: "Key is empty : Private key is empty in current request.",
    2: "Incorrect Key : Private key is wrong/incorrect format.",
    3: "Wrong type : Requesting an incorrect basic type.",
    4: "Wrong fields : Requesting incorrect selection fields.",
    5: "Too many requests : Requests are blocked for a small period of time because of too many requests per user (max 100 per minute).",
    6: "Incorrect ID : Wrong ID value.",
    7: "Incorrect ID-entity relation : A requested selection is private (For example, personal data of another user / faction).",
    8: "IP block : Current IP is banned for a small period of time because of abuse.",
    9: "API disabled : Api system is currently disabled.",
    10: "Key owner is in federal jail : Current key can't be used because owner is in federal jail.",
    11: "Key change error : You can only change your API key once every 60 seconds.",
    12: "Key read error : Error reading key from Database.",
    13: "The key is temporarily disabled due to owner inactivity : The key owner hasn't been online for more than 7 days.",
    14: "Daily read limit reached : Too many records have been pulled today by this user from our cloud services.",
    15: "Temporary error : An error code specifically for testing purposes that has no dedicated meaning.",
    16: "Access level of this key is not high enough : A selection is being called of which this key does not have permission to access.",
    17: "Backend error occurred, please try again."
}


# api错误规范
class ApiException(Exception):
    def __init__(self, code, message, status_code):
        super().__init__(message)
        self.code = code
        self.status_code = status_code

    def to_dict(self):
        return {'code': self.code, 'error': self.args[0]}

    def __str__(self):
        return f"{self.code}: {self.args[0]}"


# 抛出api错误
def throw_api_error(code: int, msg: str, status_code: status) -> tuple:
    try:
        raise ApiException(code, msg, status_code)
    except ApiException as e:
        return e.to_dict(), e.status_code


class TornApi:
    def __init__(self):
        self.test_key = self.get_test_key()
        self.key = ''
        self.api_type = ''
        self.query_id = ''
        self.Selections = ''
        self.url = ''
        self.error_description = ERROR_DESCRIPTION

    def get_info(self, api_type, selections='', query_id='', key=None):
        # 生产环境key默认为空, 需要前端传key,测试环境可以通过config文件
        if self.check_key_is_required() and key is None:
            return throw_api_error(99, 'Key is empty', status.HTTP_400_BAD_REQUEST)
        self.api_type = api_type
        self.query_id = query_id
        self.Selections = selections
        self.url = f'https://api.torn.com/{self.api_type}/{self.query_id}?selections={self.Selections}&key={self.key}'
        print(f'开始请求：{self.url}')
        try:
            data = requests.get(self.url).json()
        except Exception as e:
            # todo 待完善
            print('error--:', e)
            return e
        # torn api 返回错误处理
        if data.get('error', None):
            return throw_api_error(99, self.get_error_description(data.error.code), status.HTTP_200_OK)
        return data

    @classmethod
    def get_test_key(cls):
        return TORN_API_KEY if IS_TESTING_SERVICE else None

    def check_key_is_required(self):
        if IS_TESTING_SERVICE and self.test_key is None:
            return True
        if not IS_TESTING_SERVICE:
            return True
        return False

    def get_error_description(self, code):
        return getattr(self.error_description, code)
