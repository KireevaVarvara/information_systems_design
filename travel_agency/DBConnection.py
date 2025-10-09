import threading
from typing import Optional

import psycopg2


class DBConnection:
    _instance: Optional["DBConnection"] = None
    _lock = threading.Lock()
    _connection = None

    def __new__(cls):
        """Гарантирует создание только одного экземпляра класса"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            self._host = "localhost"
            self._port = 5433
            self._database = "travel_agency"
            self._user = "postgres"
            self._password = "123"

    def configure(self, host: str, port: int, database: str, user: str, password: str):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._password = password

    def connect(self):
        """Установка соединения с БД"""
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(
                    host=self._host, port=self._port, database=self._database, user=self._user, password=self._password
                )
                print(f"✓ Подключение к БД {self._database} установлено")
            except psycopg2.Error as e:
                print(f"✗ Ошибка подключения к БД: {e}")
                raise

    def get_connection(self):
        """
        Получение активного подключения
        """
        if self._connection is None or self._connection.closed:
            self.connect()
        return self._connection

    def close(self):
        """Закрытие соединения с БД"""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            print("✓ Соединение с БД закрыто")

    def execute_query(self, query: str, params: tuple = None, fetch: bool = True):
        """
        Выполнение SQL запроса
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)

            if fetch:
                result = cursor.fetchall()
                cursor.close()
                return result
            else:
                conn.commit()
                cursor.close()
                return None

        except psycopg2.Error as e:
            conn.rollback()
            cursor.close()
            raise Exception(f"Ошибка выполнения запроса: {e}")

    def execute_query_one(self, query: str, params: tuple = None):
        """
        Выполнение SQL запроса с возвратом одной записи
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result

        except psycopg2.Error as e:
            cursor.close()
            raise Exception(f"Ошибка выполнения запроса: {e}")
