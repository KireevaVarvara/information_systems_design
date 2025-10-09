import json
import re

from travel_agency.BaseClient import BaseClient


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        phone_number = kwargs.pop("phone_number", None)
        pasport = kwargs.pop("pasport", None)
        email = kwargs.pop("email", None)
        balance = kwargs.pop("balance", None)

        super().__init__(*args, **kwargs)

        self.set_phone_number(phone_number)
        self.set_pasport(pasport)
        self.set_email(email)
        self.set_balance(balance)

    def set_phone_number(self, phone_number):
        self._phone_number = self._validate_phone_number(phone_number)

    def set_pasport(self, pasport):
        self._pasport = self._validate_pasport(pasport)

    def set_email(self, email):
        self._email = self._validate_email(email)

    def set_balance(self, balance):
        self._balance = self._validate_balance(balance)

    def get_phone_number(self):
        return self._phone_number

    def get_pasport(self):
        return self._pasport

    def get_email(self):
        return self._email

    def get_balance(self):
        return self._balance

    @staticmethod
    def _validate_phone_number(phone_number):
        if phone_number is None:
            return None
        if not isinstance(phone_number, str) or not re.fullmatch(
            r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", phone_number
        ):
            raise ValueError("Неверный номер телефона")
        return phone_number

    @staticmethod
    def _validate_pasport(pasport):
        if pasport is None:
            return None
        if not isinstance(pasport, str) or not re.fullmatch(r"\d{4} \d{6}", pasport):
            raise ValueError("Неверные паспортные данные. Формат: XXXX XXXXXX")
        return pasport

    @staticmethod
    def _validate_email(email):
        if email is None:
            return None
        if not isinstance(email, str) or not re.fullmatch(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", email):
            raise ValueError("Неверный email")
        return email

    @staticmethod
    def _validate_balance(balance):
        if balance is not None:
            if not isinstance(balance, (float, int)):
                raise ValueError("Баланс должен быть числом")
            if balance < 0:
                raise ValueError("Баланс не должен быть отрицательным")
        return balance

    @classmethod
    def from_json(cls, json_str):
        fields = json.loads(json_str)
        return cls(**fields)

    @classmethod
    def from_string(cls, string_data, delimiter=","):
        try:
            fields = string_data.split(delimiter)
            if not (8 <= len(fields) <= 9):
                raise ValueError(f"Ожидалось 8-9 полей, получено {len(fields)}")

            field_names = [
                "surname",
                "firstname",
                "fathers_name",
                "birth_date",
                "phone_number",
                "pasport",
                "email",
                "balance",
                "id",
            ]
            kwargs = {}

            for i, value in enumerate(fields):
                if i < len(field_names):
                    field_name = field_names[i]
                    value = value.strip() if value else None
                    if value and value.lower() != "none":
                        if field_name == "balance":
                            try:
                                kwargs[field_name] = float(value)
                            except ValueError:
                                raise ValueError(f"Неверный формат баланса: {value}")
                        else:
                            kwargs[field_name] = value

            return cls(**kwargs)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Ошибка парсинга строки: {e}")

    @property
    def full_information(self):
        birth_date_str = self.get_birth_date().strftime("%d.%m.%Y") if self.get_birth_date() else None
        return (
            self.get_id(),
            self.get_surname(),
            self.get_firstname(),
            self.get_fathers_name(),
            birth_date_str,
            self.get_phone_number(),
            self.get_pasport(),
            self.get_email(),
            self.get_balance(),
        )

    @property
    def short_information(self):
        birth_date_str = self.get_birth_date().strftime("%d.%m.%Y") if self.get_birth_date() else None
        return (
            self.get_id(),
            self.get_surname(),
            self.get_firstname(),
            self.get_fathers_name(),
            birth_date_str,
            self.get_email(),
        )
