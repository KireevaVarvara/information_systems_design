from typing import Any, Dict, List, Optional

from travel_agency.Client import Client

from .observer import RepositoryObserver
from .repository import ObservableClientRepository


class ClientController(RepositoryObserver):
    """
    Контроллер уровня приложения. Получает данные из репозитория через
    паттерн Наблюдатель и подготавливает DTO для представления.
    """

    def __init__(self, repository: ObservableClientRepository):
        self.repository = repository
        self.repository.subscribe(self)
        self._last_payload: Dict[str, Any] = {}

    def update(self, event: str, payload: Any) -> None:
        self._last_payload[event] = payload

    def get_clients_overview(self) -> List[Dict[str, Any]]:
        """Возвращает краткую информацию о клиентах для таблицы."""
        self._last_payload.pop("clients_loaded", None)
        self.repository.read_all()
        clients: List[Client] = self._last_payload.get("clients_loaded", [])
        return [self._short_dto(client) for client in clients]

    def get_client_details(self, client_id: Any) -> Optional[Dict[str, Any]]:
        """Возвращает полную информацию о клиенте для отдельной вкладки."""
        self._last_payload.pop("client_loaded", None)
        self.repository.get_by_id(client_id)
        client: Optional[Client] = self._last_payload.get("client_loaded")
        if client is None:
            return None
        return self._full_dto(client)

    @staticmethod
    def _short_dto(client: Client) -> Dict[str, Any]:
        birth_date = client.get_birth_date()
        return {
            "id": client.get_id(),
            "surname": client.get_surname(),
            "firstname": client.get_firstname(),
            "email": client.get_email(),
            "birth_date": birth_date.strftime("%d.%m.%Y") if birth_date else None,
        }

    @staticmethod
    def _full_dto(client: Client) -> Dict[str, Any]:
        birth_date = client.get_birth_date()
        return {
            "id": client.get_id(),
            "surname": client.get_surname(),
            "firstname": client.get_firstname(),
            "fathers_name": client.get_fathers_name(),
            "birth_date": birth_date.strftime("%d.%m.%Y") if birth_date else None,
            "phone_number": client.get_phone_number(),
            "pasport": client.get_pasport(),
            "email": client.get_email(),
            "balance": client.get_balance(),
        }


class ClientCreateController(RepositoryObserver):
    """
    Отдельный контроллер для окна создания клиента.
    Подписан на репозиторий и валидирует входные данные через доменную модель.
    """

    def __init__(self, repository: ObservableClientRepository):
        self.repository = repository
        self.repository.subscribe(self)
        self._last_payload: Dict[str, Any] = {}

    def update(self, event: str, payload: Any) -> None:
        self._last_payload[event] = payload

    def create_client(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            client = Client(**payload)
        except Exception as error:
            raise ValueError(str(error))

        self._last_payload.pop("client_added", None)
        created = self.repository.add_client(client)
        registered = self._last_payload.get("client_added", created)
        return ClientController._full_dto(registered)
