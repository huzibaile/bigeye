import json


def calculate_mug_amount(file_path):
    with open(file_path) as f:
        data = json.load(f)

    logs = data.get('logs')

    return sum([log.get('data').get('money_mugged') for log in logs])


def calculate_bounty_amount(file_path):
    with open(file_path) as f:
        data = json.load(f)
        logs = data.get('logs')
        return sum([log.get('data').get('cost') for log in logs])


if __name__ == '__main__':
    print(calculate_bounty_amount('torn-log-2876307-1686065100.json'))
