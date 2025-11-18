from abc import ABC, abstractmethod
from typing import List, Optional

from travel_agency.Client import Client


class Client_rep_base(ABC):
    """
    Абстрактный базовый класс для репозиториев клиентов.
    Определяет общий интерфейс для работы с различными форматами хранения данных.
    """

    def __init__(self, file_path: str):
        """
        Инициализация репозитория.

        Args:
            file_path: Путь к файлу для хранения данных
        """
        self.file_path = file_path
        self._clients: List[Client] = []
        self._load_from_file()

    @abstractmethod
    def _load_from_file(self):
        """Чтение всех значений из файла (абстрактный метод)"""
        pass

    @abstractmethod
    def write_all(self):
        """b. Запись всех значений в файл (абстрактный метод)"""
        pass

    def reload_from_file(self):
        """Принудительная перезагрузка данных из файла"""
        self._load_from_file()

    def read_all(self) -> List[Client]:
        """
        a. Получить все клиенты из памяти

        Returns:
            Список всех объектов Client (копия внутреннего списка)

        Note:
            Метод возвращает текущее состояние данных в памяти.
            Для перезагрузки данных из файла используйте reload_from_file()
        """
        return self._clients.copy()

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        c. Получить объект по ID

        Args:
            client_id: ID клиента

        Returns:
            Объект Client или None, если не найден
        """
        for client in self._clients:
            if client.get_id() == client_id:
                return client
        return None

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        d. Получить список k по счету n объектов класса short
        (например, вторые 20 элементов для листания длинного списка)

        Args:
            k: Номер страницы (начиная с 1)
            n: Количество элементов на странице

        Returns:
            Список кортежей с краткой информацией о клиентах
        """
        start_index = (k - 1) * n
        end_index = start_index + n

        if start_index >= len(self._clients):
            return []

        page_clients = self._clients[start_index:end_index]
        return [client.short_information for client in page_clients]

    @abstractmethod
    def sort_by_field(self, reverse: bool = False):
        """
        e. Сортировать элементы по выбранному полю (абстрактный метод)

        Args:
            reverse: Если True, сортировка в обратном порядке
        """
        pass

    def add_client(self, client: Client) -> Client:
        """
        f. Добавить объект в список (при добавлении сформировать новый ID)

        Args:
            client: Объект Client для добавления

        Returns:
            Добавленный клиент с новым ID
        """
        # Генерация нового ID
        if self._clients:
            max_id = max(c.get_id() for c in self._clients)
            new_id = max_id + 1
        else:
            new_id = 1

        # Создание нового клиента с новым ID
        birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else None

        new_client = Client(
            id=new_id,
            surname=client.get_surname(),
            firstname=client.get_firstname(),
            fathers_name=client.get_fathers_name(),
            birth_date=birth_date_str,
            phone_number=client.get_phone_number(),
            pasport=client.get_pasport(),
            email=client.get_email(),
            balance=client.get_balance(),
        )

        self._clients.append(new_client)
        self.write_all()
        return new_client

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """
        g. Заменить элемент списка по ID

        Args:
            client_id: ID клиента для замены
            new_client: Новый объект Client

        Returns:
            True если замена успешна, False если клиент не найден
        """
        for i, client in enumerate(self._clients):
            if client.get_id() == client_id:
                # Создаем нового клиента с сохранением ID
                birth_date_str = (
                    new_client.get_birth_date().strftime("%d.%m.%Y") if new_client.get_birth_date() else None
                )

                updated_client = Client(
                    id=client_id,
                    surname=new_client.get_surname(),
                    firstname=new_client.get_firstname(),
                    fathers_name=new_client.get_fathers_name(),
                    birth_date=birth_date_str,
                    phone_number=new_client.get_phone_number(),
                    pasport=new_client.get_pasport(),
                    email=new_client.get_email(),
                    balance=new_client.get_balance(),
                )

                self._clients[i] = updated_client
                self.write_all()
                return True
        return False

    def delete_by_id(self, client_id: int) -> bool:
        """
        h. Удалить элемент списка по ID

        Args:
            client_id: ID клиента для удаления

        Returns:
            True если удаление успешно, False если клиент не найден
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

        Returns:
            Количество клиентов в списке
        """
        return len(self._clients)
