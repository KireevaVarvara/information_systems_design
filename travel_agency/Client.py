import re
import json

from travel_agency.Client_short_info import Client_short_info

class Client(Client_short_info):
    def __init__(self, firstname, surname, fathers_name, phone_number, pasport, email, balance=None):
        super(Client, self).__init__(firstname=firstname, surname=surname, fathers_name=fathers_name, email=email)
        self.set_phone_number(phone_number)
        self.set_pasport(pasport)
        self.set_balance(balance)

    def set_phone_number(self, phone_number):
        self._phone_number = self.__validate_phone_number(phone_number)
    def set_pasport(self, pasport):
        self._pasport = self.__validate_pasport(pasport)
    def set_balance(self, balance):
        self._balance = self.__validate_balance(balance)

    def get_phone_number(self):
        return self._phone_number
    def get_pasport(self):
        return self._pasport
    def get_balance(self):
        return self._balance

    @staticmethod
    def __validate_phone_number(phone_number):
        if not isinstance(phone_number, str) or not re.fullmatch(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', phone_number):
            raise ValueError('Неверный номер телефона')
        return phone_number

    @staticmethod
    def __validate_pasport(pasport):
        if not isinstance(pasport, str) or not re.fullmatch(r'\d{4} \d{6}', pasport):
            raise ValueError('Неверные паспортные данные')
        return pasport

    @staticmethod
    def __validate_balance(balance):
        if balance is not None:
            if not isinstance(balance, (float, int)):
                raise ValueError('Баланс должен быть числом')
            if balance < 0:
                raise ValueError('Баланс не должен быть отрицательным')
        return balance

    @classmethod
    def from_json(cls, json_str):
        fields = json.loads(json_str)
        return cls(
            firstname=fields['firstname'],
            surname=fields['surname'],
            fathers_name=fields['fathers_name'],
            phone_number=fields['phone_number'],
            pasport=fields['pasport'],
            email=fields['email'],
            balance=fields['balance'],
        )

    @property
    def full_information(self):
        return (
            self.get_firstname(),
            self.get_surname(),
            self.get_fathers_name(),
            self.get_phone_number(),
            self.get_pasport(),
            self.get_email(),
            self.get_balance(),
        )

    @property
    def short_information(self):
        return (
            self.get_firstname(),
            self.get_surname(),
            self.get_fathers_name(),
            self.get_email(),
        )