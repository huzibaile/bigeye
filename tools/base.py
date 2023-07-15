# 压扁字典
from _decimal import Decimal, ROUND_HALF_UP


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
