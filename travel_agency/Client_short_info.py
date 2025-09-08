import re

class Client_short_info:
    def __init__(self, firstname, surname, fathers_name, email):
        self.set_firstname(firstname)
        self.set_surname(surname)
        self.set_fathers_name(fathers_name)
        self.set_email(email)

    def set_firstname(self, firstname):
        self._firstname = self.__validate_fio(firstname)
    def set_surname(self, surname):
        self._surname = self.__validate_fio(surname)
    def set_fathers_name(self, fathers_name):
        self._fathers_name = self.__validate_fio(fathers_name, True)
    def set_email(self, email):
        self._email = self.__validate_email(email)

    def get_firstname(self):
        return self._firstname
    def get_surname(self):
        return self._surname
    def get_fathers_name(self):
        return self._fathers_name
    def get_email(self):
        return self._email

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
    def __validate_email(email):
        if not isinstance(email, str) or not re.fullmatch(r'([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', email):
            raise ValueError('Неверный email')
        return email

    def __eq__(self, other):
        if any((
                self.get_firstname() != other.get_firstname(),
                self.get_surname() != other.get_surname(),
                self.get_fathers_name() != other.get_fathers_name(),
                self.get_email() != other.get_email(),
        )):
            return False
        return True

    def __str__(self):
        return f'{self.get_surname} {self.get_firstname}'