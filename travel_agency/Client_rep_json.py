import json
import os

from travel_agency.Client import Client
from travel_agency.Client_rep_base import Client_rep_base


class Client_rep_json(Client_rep_base):
    def _load_from_file(self):
        """Чтение всех значений из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._clients = [Client.from_json(json.dumps(item, ensure_ascii=False)) for item in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self._clients = []
        else:
            self._clients = []

    def write_all(self):
        """b. Запись всех значений в файл"""
        data = []
        for client in self._clients:
            birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else None
            client_data = {
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
            data.append(client_data)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def sort_by_field(self, reverse: bool = False):
        """Переопределение абстрактного метода - сортировка по email"""
        self.sort_by_email(reverse)

    def sort_by_email(self, reverse: bool = False):
        """
        e. Сортировать элементы по выбранному полю (email)
        """
        self._clients.sort(key=lambda client: client.get_email() if client.get_email() else "", reverse=reverse)
