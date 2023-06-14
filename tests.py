import unittest
import json
from datetime import datetime
from main import format_number, process_json


class TestFormatNumber(unittest.TestCase):
    def test_format_number_with_none(self):
        self.assertEqual(format_number(None), '')

    def test_format_number_with_account(self):
        self.assertEqual(format_number('Перевод на счет 1234567812345678'), 'Перевод на счет **5678')

    def test_format_number_with_card(self):
        self.assertEqual(format_number('Оплата товаров и услуг по карте 1234561238497890'), 'Оплата товаров и услуг по карте 1234 56** **** 7890')


class TestProcessJSON(unittest.TestCase):
    def setUp(self):
        self.data = [
            {
                "state": "EXECUTED",
                "date": "2022-01-01T10:00:00.000000",
                "description": "Покупка",
                "from": "Оплата товаров и услуг по карте 1234567812345678",
                "to": "Перевод на счет 1234567812345678",
                "operationAmount": {
                    "amount": 1000,
                    "currency": {
                        "name": "RUB"
                    }
                }
            },
            {
                "state": "EXECUTED",
                "date": "2022-01-02T10:00:00.000000",
                "description": "Перевод",
                "from": None,
                "to": "Перевод на счет 1234567812345678",
                "operationAmount": {
                    "amount": 2000,
                    "currency": {
                        "name": "RUB"
                    }
                }
            },
            {
                "state": "CANCELED",
                "date": "2022-01-03T10:00:00.000000",
                "description": "Покупка",
                "from": "Оплата товаров и услуг по карте 1234567812345678",
                "to": "Перевод на счет 1234567812345678",
                "operationAmount": {
                    "amount": 3000,
                    "currency": {
                        "name": "RUB"
                    }
                }
            },
            {
                "state": "EXECUTED",
                "date": "2022-01-04T10:00:00.000000",
                "description": "Перевод",
                "from": None,
                "to": "Перевод на счет 1234567812345678",
                "operationAmount": {
                    "amount": 4000,
                    "currency": {
                        "name": "RUB"
                    }
                }
            },
            {
                "state": "EXECUTED",
                "date": "2022-01-05T10:00:00.000000",
                "description": "Покупка",
                "from": None,
                "to": "Счет 1234567812345678",
                "operationAmount": {
                    "amount": 5000,
                    "currency": {
                        "name": "RUB"
                    }
                }
            }
        ]

        with open('test_operations.json', 'w') as file:
            json.dump(self.data, file)

    def test_process_json(self):
        self.maxDiff = None
        expected_result = """01.01.2022 Покупка
Оплата товаров и услуг по карте 1234 56** **** 5678 -> Перевод на счет **5678
1000 RUB

02.01.2022 Перевод
Перевод на счет **5678
2000 RUB

04.01.2022 Перевод
Перевод на счет **5678
4000 RUB

05.01.2022 Покупка
Счет **5678
5000 RUB"""
        self.assertEqual(process_json('test_operations.json'), expected_result)


if __name__ == '__main__':
    unittest.main()

