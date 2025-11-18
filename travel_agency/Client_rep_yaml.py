import os

import yaml

from travel_agency.Client import Client
from travel_agency.Client_rep_base import Client_rep_base


class Client_rep_yaml(Client_rep_base):
    """
    Класс для работы с данными клиентов в формате YAML.
    Обеспечивает чтение, запись, поиск, сортировку и управление объектами Client.
    Наследуется от Client_rep_base.
    """

    def _load_from_file(self):
        """Чтение всех значений из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        self._clients = [self._dict_to_client(item) for item in data]
                    else:
                        self._clients = []
            except (yaml.YAMLError, FileNotFoundError):
                self._clients = []
        else:
            self._clients = []

    def _dict_to_client(self, data: dict) -> Client:
        """Преобразование словаря в объект Client"""
        return Client(
            id=data.get("id"),
            surname=data.get("surname"),
            firstname=data.get("firstname"),
            fathers_name=data.get("fathers_name"),
            birth_date=data.get("birth_date"),
            phone_number=data.get("phone_number"),
            pasport=data.get("pasport"),
            email=data.get("email"),
            balance=data.get("balance"),
        )

    def _client_to_dict(self, client: Client) -> dict:
        """Преобразование объекта Client в словарь"""
        birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else None
        return {
            "id": client.get_id(),
            "surname": client.get_surname(),
            "firstname": client.get_firstname(),
            "fathers_name": client.get_fathers_name(),
            "birth_date": birth_date_str,
            "phone_number": client.get_phone_number(),
            "pasport": client.get_pasport(),
            "email": client.get_email(),
            "balance": client.get_balance(),
        }

    def write_all(self):
        """b. Запись всех значений в файл"""
        data = [self._client_to_dict(client) for client in self._clients]

        with open(self.file_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def sort_by_field(self, reverse: bool = False):
        """Переопределение абстрактного метода - сортировка по фамилии"""
        self.sort_by_surname(reverse)

    def sort_by_surname(self, reverse: bool = False):
        """
        e. Сортировать элементы по выбранному полю (surname/фамилия)

        Args:
            reverse: Если True, сортировка в обратном порядке
        """
        self._clients.sort(key=lambda client: client.get_surname() if client.get_surname() else "", reverse=reverse)
