import re
import json

class Client:
    def __init__(self, firstname, surname, fathers_name, phone_number, pasport, email, balance=None):
        self.set_firstname(firstname)
        self.set_surname(surname)
        self.set_fathers_name(fathers_name)
        self.set_phone_number(phone_number)
        self.set_pasport(pasport)
        self.set_email(email)
        self.set_balance(balance)

    def set_firstname(self, firstname):
        self._firstname = self.__validate_fio(firstname)
    def set_surname(self, surname):
        self._surname = self.__validate_fio(surname)
    def set_fathers_name(self, fathers_name):
        self._fathers_name = self.__validate_fio(fathers_name, True)
    def set_phone_number(self, phone_number):
        self._phone_number = self.__validate_phone_number(phone_number)
    def set_pasport(self, pasport):
        self._pasport = self.__validate_pasport(pasport)
    def set_email(self, email):
        self._email = self.__validate_email(email)
    def set_balance(self, balance):
        self._balance = self.__validate_balance(balance)

    def get_firstname(self):
        return self._firstname
    def get_surname(self):
        return self._surname
    def get_fathers_name(self):
        return self._fathers_name
    def get_phone_number(self):
        return self._phone_number
    def get_pasport(self):
        return self._pasport
    def get_email(self):
        return self._email
    def get_balance(self):
        return self._balance

    @staticmethod
    def __validate_fio(fio_field, is_fathers_name=False):
        if not isinstance(fio_field, str) and not is_fathers_name:
            raise ValueError('Имя и фамилия должны быть строковыми')
        if not fio_field and not is_fathers_name:
            raise ValueError('ФИО не должно быть пустым')
        if ((is_fathers_name and fio_field is not None) or not is_fathers_name) and re.search(r'\d', fio_field) is not None:
            raise ValueError('ФИО не должно содержать цифр')
        return fio_field

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
    def __validate_email(email):
        if not isinstance(email, str) or not re.fullmatch(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', email):
            raise ValueError('Неверный email')
        return email

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

    def __str__(self):
        return f'{self._surname} {self._firstname}'