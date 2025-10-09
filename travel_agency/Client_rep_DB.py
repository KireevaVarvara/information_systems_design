from typing import List, Optional

from travel_agency.Client import Client
from travel_agency.DBConnection import DBConnection


class Client_rep_DB:
    def __init__(self):
        """Инициализация репозитория с подключением к БД"""
        self.db = DBConnection()

    def _row_to_client(self, row: tuple) -> Client:
        """
        Преобразование строки из БД в объект Client
        """
        birth_date_str = row[4].strftime("%d.%m.%Y") if row[4] else None

        return Client(
            id=row[0],
            surname=row[1],
            firstname=row[2],
            fathers_name=row[3],
            birth_date=birth_date_str,
            phone_number=row[5],
            pasport=row[6],
            email=row[7],
            balance=float(row[8]) if row[8] else None,
        )

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        a. Получить объект по ID
        """
        query = """
            SELECT id, surname, firstname, fathers_name, birth_date,
                   phone_number, pasport, email, balance
            FROM clients
            WHERE id = %s
        """

        try:
            row = self.db.execute_query_one(query, (client_id,))
            if row:
                return self._row_to_client(row)
            return None
        except Exception as e:
            print(f"Ошибка получения клиента: {e}")
            return None

    def get_k_n_short_list(self, k: int, n: int) -> List[tuple]:
        """
        b. Получить список k по счету n объектов класса short
        """
        offset = (k - 1) * n

        query = """
            SELECT id, surname, firstname, fathers_name, birth_date, email
            FROM clients
            ORDER BY id
            LIMIT %s OFFSET %s
        """

        try:
            rows = self.db.execute_query(query, (n, offset))
            # Возвращаем в формате short_information
            result = []
            for row in rows:
                # (id, surname, firstname, fathers_name, birth_date, email)
                birth_date_str = row[4].strftime("%d.%m.%Y") if row[4] else None
                result.append((row[0], row[1], row[2], row[3], birth_date_str, row[5]))
            return result
        except Exception as e:
            print(f"Ошибка получения списка: {e}")
            return []

    def add_client(self, client: Client) -> Optional[Client]:
        """
        c. Добавить объект в список (ID генерируется автоматически БД)
        """
        query = """
            INSERT INTO clients (surname, firstname, fathers_name, birth_date,
                                phone_number, pasport, email, balance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, surname, firstname, fathers_name, birth_date,
                      phone_number, pasport, email, balance
        """

        # Преобразование даты рождения
        birth_date = None
        if client.get_birth_date():
            birth_date = client.get_birth_date().strftime("%Y-%m-%d")

        params = (
            client.get_surname(),
            client.get_firstname(),
            client.get_fathers_name(),
            birth_date,
            client.get_phone_number(),
            client.get_pasport(),
            client.get_email(),
            client.get_balance(),
        )

        try:
            row = self.db.execute_query_one(query, params)
            if row:
                return self._row_to_client(row)
            return None
        except Exception as e:
            print(f"Ошибка добавления клиента: {e}")
            return None

    def replace_by_id(self, client_id: int, new_client: Client) -> bool:
        """
        d. Заменить элемент списка по ID
        """
        query = """
            UPDATE clients
            SET surname = %s, firstname = %s, fathers_name = %s, birth_date = %s,
                phone_number = %s, pasport = %s, email = %s, balance = %s
            WHERE id = %s
        """

        # Преобразование даты рождения
        birth_date = None
        if new_client.get_birth_date():
            birth_date = new_client.get_birth_date().strftime("%Y-%m-%d")

        params = (
            new_client.get_surname(),
            new_client.get_firstname(),
            new_client.get_fathers_name(),
            birth_date,
            new_client.get_phone_number(),
            new_client.get_pasport(),
            new_client.get_email(),
            new_client.get_balance(),
            client_id,
        )

        try:
            self.db.execute_query(query, params, fetch=False)
            return True
        except Exception as e:
            print(f"Ошибка замены клиента: {e}")
            return False

    def delete_by_id(self, client_id: int) -> bool:
        """
        e. Удалить элемент списка по ID
        """
        query = "DELETE FROM clients WHERE id = %s"

        try:
            self.db.execute_query(query, (client_id,), fetch=False)
            return True
        except Exception as e:
            print(f"Ошибка удаления клиента: {e}")
            return False

    def get_count(self) -> int:
        """
        f. Получить количество элементов
        """
        query = "SELECT COUNT(*) FROM clients"

        try:
            row = self.db.execute_query_one(query)
            return row[0] if row else 0
        except Exception as e:
            print(f"Ошибка получения количества: {e}")
            return 0

    def read_all(self) -> List[Client]:
        """
        Получить все записи из БД
        """
        query = """
            SELECT id, surname, firstname, fathers_name, birth_date,
                   phone_number, pasport, email, balance
            FROM clients
            ORDER BY id
        """

        try:
            rows = self.db.execute_query(query)
            return [self._row_to_client(row) for row in rows]
        except Exception as e:
            print(f"Ошибка чтения всех клиентов: {e}")
            return []
