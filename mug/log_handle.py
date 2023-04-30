import json


def calculate_mug_amount(file_path):
    with open(file_path) as f:
        data = json.load(f)

    logs = data.get('logs')

    return sum([log.get('data').get('money_mugged') for log in logs])


print(calculate_mug_amount('torn-log-2893342-1682738866.json'))
