from typing import Any, List, Protocol


class RepositoryObserver(Protocol):
    """Протокол наблюдателя, который реагирует на события репозитория."""

    def update(self, event: str, payload: Any) -> None:
        ...


class ObservableRepositoryMixin:
    """Примесь, добавляющая поддержку паттерна Наблюдатель к репозиторию."""

    def __init__(self, *args, **kwargs):
        self._observers: List[RepositoryObserver] = []
        super().__init__(*args, **kwargs)

    def subscribe(self, observer: RepositoryObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: RepositoryObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, event: str, payload: Any) -> None:
        for observer in list(self._observers):
            observer.update(event, payload)

