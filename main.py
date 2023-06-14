import json
from datetime import datetime


def format_number(s):
    if s is None:
        return ''
    tmp_from = s.split()[-1]
    if "счет" in s.lower():
        return f"{s[:-len(s.split()[-1])].strip()} **{s[-4:]}"
    else:
        return f"{s[:-len(s.split()[-1])].strip()} {tmp_from[0:4]} {tmp_from[4:6]}** **** {tmp_from[12:16]}"


def process_json(file_path):
    mas = {}

    with open(file_path) as file:
        data = json.load(file)

    for ex in data:
        if ex.get('state') == 'EXECUTED':
            date = datetime.strptime(ex['date'], '%Y-%m-%dT%H:%M:%S.%f')
            description = ex['description']
            from_ = format_number(ex.get('from'))
            to_ = format_number(ex['to'])
            amount = ex['operationAmount']['amount']
            currency = ex['operationAmount']['currency']['name']
            mas[date] = f"{date.strftime('%d.%m.%Y')} {description}\n{from_}{' -> ' if from_ else ''}{to_}\n{amount} {currency}"

    new_dict = sorted(mas.items(), key=lambda item: item[0])

    return "\n\n".join([i[1] for i in new_dict[-5:]])


if __name__ == "__main__":
    print(process_json('operations.json'))

