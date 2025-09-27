import re
import uuid
import json
from datetime import datetime

class BaseClient:
    def __init__(self, *args, **kwargs):
        if args and len(args) >= 4:
            surname, firstname, fathers_name, birth_date = args[0], args[1], args[2], args[3]
            id = args[4] if len(args) > 4 else None
        else:
            surname = kwargs.get('surname')
            firstname = kwargs.get('firstname')
            fathers_name = kwargs.get('fathers_name')
            birth_date = kwargs.get('birth_date')
            id = kwargs.get('id')

        if id is None:
            id = self._generate_id()
        self.set_id(id)
        self.set_surname(surname)
        self.set_firstname(firstname)
        self.set_fathers_name(fathers_name)
        self.set_birth_date(birth_date)

    def set_id(self, id):
        self._id = self._validate_id(id)
    def set_surname(self, surname):
        self._surname = self._validate_fio(surname)
    def set_firstname(self, firstname):
        self._firstname = self._validate_fio(firstname)
    def set_fathers_name(self, fathers_name):
        self._fathers_name = self._validate_fio(fathers_name, True)
    def set_birth_date(self, birth_date):
        self._birth_date = self._validate_birth_date(birth_date)

    def get_id(self):
        return self._id
    def get_surname(self):
        return self._surname
    def get_firstname(self):
        return self._firstname
    def get_fathers_name(self):
        return self._fathers_name
    def get_birth_date(self):
        return self._birth_date

    @staticmethod
    def _validate_id(id):
        if isinstance(id, int) and id > 0:
            return id
        elif isinstance(id, str) and len(id) == 16:
            return id
        else:
            raise ValueError('Неверный ID. Должен быть положительным int или UUID строкой')

    @classmethod
    def _generate_id(cls):
        return uuid.uuid4().hex[:16]

    @staticmethod
    def _validate_fio(fio_field, is_fathers_name=False):
        if not isinstance(fio_field, str) and not is_fathers_name:
            raise ValueError('Имя и фамилия должны быть строковыми')
        if not fio_field and not is_fathers_name:
            raise ValueError('ФИО не должно быть пустым')
        if ((is_fathers_name and fio_field is not None) or not is_fathers_name) and re.search(r'\d', fio_field) is not None:
            raise ValueError('ФИО не должно содержать цифр')
        return fio_field

    @staticmethod
    def _validate_birth_date(birth_date):
        if birth_date is None:
            return None
        if isinstance(birth_date, str):
            try:
                return datetime.strptime(birth_date, '%d.%m.%Y').date()
            except ValueError:
                raise ValueError('Неверный формат даты. Используйте ДД.ММ.ГГГГ')
        elif isinstance(birth_date, datetime):
            return birth_date.date()
        else:
            raise ValueError('Дата рождения должна быть строкой в формате ДД.ММ.ГГГГ или datetime объектом')

    @classmethod
    def from_json(cls, json_str):
        fields = json.loads(json_str)
        return cls(**fields)

    @classmethod
    def from_string(cls, string_data, delimiter=','):
        try:
            fields = string_data.split(delimiter)
            if not (4 <= len(fields) <= 5):
                raise ValueError(f"Ожидалось 4-5 полей, получено {len(fields)}")

            field_names = ['surname', 'firstname', 'fathers_name', 'birth_date', 'id']
            kwargs = {}

            for i, value in enumerate(fields):
                if i < len(field_names):
                    field_name = field_names[i]
                    value = value.strip() if value else None
                    if value and value.lower() != 'none':
                        kwargs[field_name] = value

            return cls(**kwargs)
        except (ValueError, IndexError) as e:
            raise ValueError(f"Ошибка парсинга строки: {e}")

    def __eq__(self, other):
        if not isinstance(other, BaseClient):
            return False
        return (self.get_surname().lower() == other.get_surname().lower() and
                self.get_firstname().lower() == other.get_firstname().lower() and
                self.get_fathers_name() == other.get_fathers_name() and
                self.get_birth_date() == other.get_birth_date())

    def __str__(self):
        birth_info = f", {self.get_birth_date().strftime('%d.%m.%Y')}" if self.get_birth_date() else ""
        return f'{self.get_id()} {self.get_surname()} {self.get_firstname()}{birth_info}'

    @property
    def short_information(self):
        birth_date_str = self.get_birth_date().strftime('%d.%m.%Y') if self.get_birth_date() else None
        return (
            self.get_id(),
            self.get_surname(),
            self.get_firstname(),
            self.get_fathers_name(),
            birth_date_str,
        )

    @property
    def full_information(self):
        return self.short_information