from typing import List, Optional

from travel_agency.Client import Client
from travel_agency.Client_rep_base import Client_rep_base
from travel_agency.Client_rep_DB import Client_rep_DB


class Client_rep_DB_adapter(Client_rep_base):
    def __init__(self):
        self.file_path = "database"  # Для совместимости с базовым классом
        self._clients: List[Client] = []
        self._db_repo = Client_rep_DB()

    def _load_from_file(self):
        """
        Переопределение абстрактного метода.
        Загрузка данных из БД вместо файла.
        """
        self._clients = self._db_repo.read_all()

    def write_all(self):
        """
        Переопределение абстрактного метода.
        Для БД не требуется массовая запись, так как все операции выполняются сразу.
        """
        # В БД данные записываются немедленно при каждой операции
        pass

    def sort_by_field(self, reverse: bool = False):
        """
        Переопределение абстрактного метода.
        Сортировка по фамилии (загружаем из БД и сортируем в памяти).
        """
        self._load_from_file()
        self._clients.sort(key=lambda client: client.get_surname() if client.get_surname() else "", reverse=reverse)

    def read_all(self) -> List[Client]:
        """
        Чтение всех клиентов из БД
        """
        return self._db_repo.read_all()

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Получить объект по ID из БД
        """
        return self._db_repo.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        Получить список k по счету n объектов
        """
        return self._db_repo.get_k_n_short_list(k, n)

    def add_client(self, client: Client) -> Client:
        """
        Добавить клиента в БД
        """
        added_client = self._db_repo.add_client(client)
        if added_client:
            return added_client
        raise Exception("Ошибка добавления клиента в БД")

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """
        Заменить клиента по ID в БД
        """
        return self._db_repo.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id: int) -> bool:
        """
        Удалить клиента по ID из БД
        """
        return self._db_repo.delete_by_id(client_id)

    def get_count(self) -> int:
        """
        Получить количество клиентов в БД
        """
        return self._db_repo.get_count()
