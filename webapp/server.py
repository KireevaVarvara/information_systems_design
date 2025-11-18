import json
import os
import urllib.parse
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from typing import Tuple

from .controller import ClientController, ClientCreateController
from .repository import ObservableClientRepository

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class ClientRequestHandler(SimpleHTTPRequestHandler):
    """
    Обработчик HTTP-запросов. Ставит API поверх контроллера и раздает статику.
    """

    def __init__(self, *args, controller: ClientController, create_controller: ClientCreateController, **kwargs):
        self.controller = controller
        self.create_controller = create_controller
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self):  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/clients":
            return self._send_clients()
        if parsed.path.startswith("/api/clients/"):
            return self._send_client_details(parsed.path)
        if parsed.path in ("/", ""):
            self.path = "/index.html"
        return super().do_GET()

    def _send_clients(self):
        clients = self.controller.get_clients_overview()
        self._json_response(200, clients)

    def _send_client_details(self, path: str):
        try:
            _, _, client_id_str = path.partition("/api/clients/")
            client_id = int(client_id_str)
        except ValueError:
            self._json_response(400, {"error": "Некорректный идентификатор"})
            return

        client = self.controller.get_client_details(client_id)
        if client is None:
            self._json_response(404, {"error": "Клиент не найден"})
            return

        self._json_response(200, client)


    def _json_response(self, status: int, payload):
        response = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        # Тише стандартного SimpleHTTPRequestHandler
        return


def build_controllers() -> Tuple[ClientController, ClientCreateController, ObservableClientRepository]:
    repository = ObservableClientRepository()
    return ClientController(repository), ClientCreateController(repository), repository


def run_server(host: str = "127.0.0.1", port: int = 8000) -> Tuple[str, int]:
    read_controller, create_controller, _ = build_controllers()
    handler = partial(ClientRequestHandler, controller=read_controller, create_controller=create_controller)
    httpd = HTTPServer((host, port), handler)
    print(f"Веб-приложение запущено: http://{host}:{port}")
    print("Главная страница: /index.html, детальная: /client.html?id=1")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        httpd.server_close()
    return host, port


if __name__ == "__main__":
    run_server()
