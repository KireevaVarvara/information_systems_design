from typing import Any, List, Optional

from travel_agency.Client import Client
from travel_agency.Client_rep_DB_adapter import Client_rep_DB_adapter

from .observer import ObservableRepositoryMixin


class ObservableClientRepository(ObservableRepositoryMixin, Client_rep_DB_adapter):
    """DB-репозиторий клиентов с уведомлением наблюдателей о чтении данных."""

    def read_all(self) -> List[Client]:
        clients = super().read_all()
        self._notify("clients_loaded", clients)
        return clients

    def get_by_id(self, client_id: Any) -> Optional[Client]:
        client = super().get_by_id(client_id)
        self._notify("client_loaded", client)
        return client