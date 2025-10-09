from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from travel_agency.Client import Client
from travel_agency.Client_rep_base import Client_rep_base


class ClientFilter(ABC):
    """Базовый класс для фильтров клиентов"""

    @abstractmethod
    def apply(self, clients: List[Client]) -> List[Client]:
        """Применить фильтр к списку клиентов"""
        pass


class BalanceFilter(ClientFilter):
    """Фильтр по балансу"""

    def __init__(self, min_balance: float = None, max_balance: float = None):
        self.min_balance = min_balance
        self.max_balance = max_balance

    def apply(self, clients: List[Client]) -> List[Client]:
        result = clients
        if self.min_balance is not None:
            result = [c for c in result if c.get_balance() and c.get_balance() >= self.min_balance]
        if self.max_balance is not None:
            result = [c for c in result if c.get_balance() and c.get_balance() <= self.max_balance]
        return result


class EmailFilter(ClientFilter):
    """Фильтр по наличию email"""

    def __init__(self, has_email: bool = True):
        self.has_email = has_email

    def apply(self, clients: List[Client]) -> List[Client]:
        if self.has_email:
            return [c for c in clients if c.get_email()]
        else:
            return [c for c in clients if not c.get_email()]


class SurnameFilter(ClientFilter):
    """Фильтр по фамилии (начинается с)"""

    def __init__(self, starts_with: str):
        self.starts_with = starts_with.lower()

    def apply(self, clients: List[Client]) -> List[Client]:
        return [c for c in clients if c.get_surname().lower().startswith(self.starts_with)]


class ClientSorter:
    """Класс для сортировки клиентов"""

    @staticmethod
    def by_surname(reverse: bool = False) -> Callable:
        """Сортировка по фамилии"""
        return lambda c: (c.get_surname() or "", reverse)

    @staticmethod
    def by_balance(reverse: bool = False) -> Callable:
        """Сортировка по балансу"""
        return lambda c: (c.get_balance() or 0, reverse)

    @staticmethod
    def by_email(reverse: bool = False) -> Callable:
        """Сортировка по email"""
        return lambda c: (c.get_email() or "", reverse)


class Client_rep_decorator(Client_rep_base):
    """
    Паттерн Декоратор (Decorator) для добавления функциональности фильтрации и сортировки.
    Декорирует любой репозиторий из иерархии Client_rep_base.
    """

    def __init__(self, repository: Client_rep_base):
        """
        Инициализация декоратора
        """
        self._repository = repository
        self.file_path = repository.file_path
        self._clients = []
        self._filters: List[ClientFilter] = []
        self._sorter: Optional[Callable] = None

    def add_filter(self, filter: ClientFilter):
        """Добавить фильтр"""
        self._filters.append(filter)

    def set_sorter(self, sorter: Callable):
        """Установить способ сортировки"""
        self._sorter = sorter

    def clear_filters(self):
        """Очистить все фильтры"""
        self._filters = []

    def clear_sorter(self):
        """Очистить сортировку"""
        self._sorter = None

    def _apply_filters_and_sorting(self, clients: List[Client]) -> List[Client]:
        """Применить фильтры и сортировку"""
        result = clients

        for filter in self._filters:
            result = filter.apply(result)

        if self._sorter:
            key_func = self._sorter
            reverse = key_func(None)[1] if callable(key_func) else False
            result = sorted(result, key=lambda c: key_func(c)[0], reverse=reverse)

        return result

    def _load_from_file(self):
        """Делегирование загрузки декорируемому объекту"""
        self._repository._load_from_file()
        self._clients = self._repository._clients

    def write_all(self):
        """Делегирование записи декорируемому объекту"""
        self._repository.write_all()

    def sort_by_field(self, reverse: bool = False):
        """Делегирование сортировки декорируемому объекту"""
        self._repository.sort_by_field(reverse)

    def read_all(self) -> List[Client]:
        """Чтение всех клиентов с применением фильтров и сортировки"""
        clients = self._repository.read_all()
        return self._apply_filters_and_sorting(clients)

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """Делегирование получения по ID"""
        return self._repository.get_by_id(client_id)

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        Получить список с пагинацией с учетом фильтров и сортировки
        """
        # Получаем все записи
        all_clients = self._repository.read_all()

        # Применяем фильтры и сортировку
        filtered_clients = self._apply_filters_and_sorting(all_clients)

        # Применяем пагинацию
        start_index = (k - 1) * n
        end_index = start_index + n

        if start_index >= len(filtered_clients):
            return []

        page_clients = filtered_clients[start_index:end_index]
        return [client.short_information for client in page_clients]

    def add_client(self, client: Client) -> Client:
        """Делегирование добавления"""
        return self._repository.add_client(client)

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """Делегирование замены"""
        return self._repository.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id: int) -> bool:
        """Делегирование удаления"""
        return self._repository.delete_by_id(client_id)

    def get_count(self) -> int:
        """
        Получить количество элементов с учетом фильтров

        Returns:
            Количество клиентов после применения фильтров
        """
        all_clients = self._repository.read_all()
        filtered_clients = self._apply_filters_and_sorting(all_clients)
        return len(filtered_clients)
