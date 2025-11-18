from typing import List, Optional

from travel_agency.Client import Client
from travel_agency.Client_rep_base import Client_rep_base
from travel_agency.Client_rep_DB import Client_rep_DB


class Client_rep_DB_adapter(Client_rep_base):
    """
    Паттерн Адаптер (Adapter) для интеграции Client_rep_DB в иерархию Client_rep_base.
    Адаптирует интерфейс работы с БД к общему интерфейсу репозиториев.
    """

    def __init__(self):
        """Инициализация адаптера с объектом Client_rep_DB"""
        # Не вызываем super().__init__(), так как не работаем с файлами
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

    def reload_from_file(self):
        """
        Переопределение метода reload_from_file.
        Для БД перезагружает данные из базы данных.
        """
        self._load_from_file()

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

        Returns:
            Список всех объектов Client
        """
        return self._db_repo.read_all()

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Получить объект по ID из БД

        Args:
            client_id: ID клиента

        Returns:
            Объект Client или None
        """
        return self._db_repo.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        Получить список k по счету n объектов

        Args:
            k: Номер страницы
            n: Количество элементов

        Returns:
            Список кортежей с краткой информацией
        """
        return self._db_repo.get_k_n_short_list(k, n)

    def add_client(self, client: Client) -> Client:
        """
        Добавить клиента в БД

        Args:
            client: Объект Client

        Returns:
            Добавленный клиент с ID
        """
        added_client = self._db_repo.add_client(client)
        if added_client:
            return added_client
        raise Exception("Ошибка добавления клиента в БД")

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """
        Заменить клиента по ID в БД

        Args:
            client_id: ID клиента
            new_client: Новый объект Client

        Returns:
            True если успешно
        """
        return self._db_repo.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id: int) -> bool:
        """
        Удалить клиента по ID из БД

        Args:
            client_id: ID клиента

        Returns:
            True если успешно
        """
        return self._db_repo.delete_by_id(client_id)

    def get_count(self) -> int:
        """
        Получить количество клиентов в БД

        Returns:
            Количество клиентов
        """
        return self._db_repo.get_count()
