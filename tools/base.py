# 压扁字典
from _decimal import Decimal, ROUND_HALF_UP
from fastapi import status


def flatten_dict(data, division='_', prefix='', dict_=None):
    if dict_ is None:
        dict_ = {}
    for key, value in data.items():
        if not isinstance(value, dict):
            dict_.update({prefix + key: value})
        else:
            flatten_dict(value, prefix=prefix + key + division, dict_=dict_)
    return dict_


# 展开字典
def expand_dict(data, division='_'):
    dict_ = {}
    for key, value in data.items():
        key_list = key.split(division)
        temp = dict_
        times = 1
        for k in key_list:
            if times == len(key_list):
                temp[k] = value
            temp[k] = {}
            temp = temp[k]
            times += 1
    return dict_


# todo 优化将配置表转换为字典
def config_table_to_dict(data, division='_'):
    dict_ = {}
    for row in data:
        key_list = row.get('name').split(division)
        temp = dict_
        for key in key_list:
            temp[key] = {}
            temp = dict_[key]
        temp = row.get('value')
    return {data[0]['config_item']: dict_}


# 精确四舍五入
def customized_rounding(number: float, digit: int = 2):
    return Decimal(number).quantize(Decimal('0.' + ('0' * digit)), rounding=ROUND_HALF_UP)


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
def throw_api_error(code: int, msg: str, status_code: status):
    try:
        raise ApiException(code, msg, status_code)
    except ApiException as e:
        return e.to_dict(), e.status_code
