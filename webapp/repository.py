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

    def add_client(self, client: Client) -> Client:
        created = super().add_client(client)
        self._notify("client_added", created)
        return created

    def update_client(self, client_id: Any, client: Client) -> Optional[Client]:
        updated = super().replace_by_id(client_id, client)
        if not updated:
            return None
        reloaded = super().get_by_id(client_id)
        self._notify("client_updated", reloaded)
        return reloaded

    def delete_client(self, client_id: Any) -> bool:
        deleted = super().delete_by_id(client_id)
        if deleted:
            self._notify("client_deleted", client_id)
        return deleted
