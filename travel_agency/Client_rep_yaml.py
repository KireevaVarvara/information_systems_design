import yaml
import os
from typing import List, Optional
from travel_agency.Client import Client


class Client_rep_yaml:
    def __init__(self, file_path: str):
        """
        Инициализация репозитория.
        """
        self.file_path = file_path
        self._clients: List[Client] = []
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
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
        return Client(
            id=data.get('id'),
            surname=data.get('surname'),
            firstname=data.get('firstname'),
            fathers_name=data.get('fathers_name'),
            birth_date=data.get('birth_date'),
            phone_number=data.get('phone_number'),
            pasport=data.get('pasport'),
            email=data.get('email'),
            balance=data.get('balance')
        )

    def _client_to_dict(self, client: Client) -> dict:
        birth_date_str = client.get_birth_date().strftime('%d.%m.%Y') if client.get_birth_date() else None
        return {
            'id': client.get_id(),
            'surname': client.get_surname(),
            'firstname': client.get_firstname(),
            'fathers_name': client.get_fathers_name(),
            'birth_date': birth_date_str,
            'phone_number': client.get_phone_number(),
            'pasport': client.get_pasport(),
            'email': client.get_email(),
            'balance': client.get_balance()
        }

    def read_all(self) -> List[Client]:
        """
        a. Чтение всех значений из файла
        """
        self._load_from_file()
        return self._clients.copy()

    def write_all(self):
        """b. Запись всех значений в файл"""
        data = [self._client_to_dict(client) for client in self._clients]

        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        c. Получить объект по ID
        """
        for client in self._clients:
            if client.get_id() == client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        d. Получить список k по счету n объектов класса short
        (например, вторые 20 элементов для листания длинного списка)
        """
        start_index = (k - 1) * n
        end_index = start_index + n

        if start_index >= len(self._clients):
            return []

        page_clients = self._clients[start_index:end_index]
        return [client.short_information for client in page_clients]

    def sort_by_surname(self, reverse: bool = False):
        """
        e. Сортировать элементы по выбранному полю (surname/фамилия)
        """
        self._clients.sort(
            key=lambda client: client.get_surname() if client.get_surname() else "",
            reverse=reverse
        )

    def add_client(self, client: Client) -> Client:
        """
        f. Добавить объект в список (при добавлении сформировать новый ID)
        """
        if self._clients:
            max_id = max(c.get_id() for c in self._clients)
            new_id = max_id + 1
        else:
            new_id = 1

        birth_date_str = client.get_birth_date().strftime('%d.%m.%Y') if client.get_birth_date() else None

        new_client = Client(
            id=new_id,
            surname=client.get_surname(),
            firstname=client.get_firstname(),
            fathers_name=client.get_fathers_name(),
            birth_date=birth_date_str,
            phone_number=client.get_phone_number(),
            pasport=client.get_pasport(),
            email=client.get_email(),
            balance=client.get_balance()
        )

        self._clients.append(new_client)
        self.write_all()
        return new_client

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """
        g. Заменить элемент списка по ID
        """
        for i, client in enumerate(self._clients):
            if client.get_id() == client_id:
                birth_date_str = new_client.get_birth_date().strftime('%d.%m.%Y') if new_client.get_birth_date() else None

                updated_client = Client(
                    id=client_id,
                    surname=new_client.get_surname(),
                    firstname=new_client.get_firstname(),
                    fathers_name=new_client.get_fathers_name(),
                    birth_date=birth_date_str,
                    phone_number=new_client.get_phone_number(),
                    pasport=new_client.get_pasport(),
                    email=new_client.get_email(),
                    balance=new_client.get_balance()
                )

                self._clients[i] = updated_client
                self.write_all()
                return True
        return False

    def delete_by_id(self, client_id: int) -> bool:
        """
        h. Удалить элемент списка по ID
        """
        for i, client in enumerate(self._clients):
            if client.get_id() == client_id:
                self._clients.pop(i)
                self.write_all()
                return True
        return False

    def get_count(self) -> int:
        """
        i. Получить количество элементов
        """
        return len(self._clients)
