"""
Демонстрация работы класса Client_rep_json
"""
from travel_agency.Client import Client
from travel_agency.Client_rep_json import Client_rep_json


def print_separator():
    print("\n" + "=" * 80)


def print_section(title):
    print_separator()
    print(f"\n{title}")
    print_separator()


def print_client(client):
    """Вывод полной информации о клиенте"""
    birth_date = client.get_birth_date().strftime('%d.%m.%Y') if client.get_birth_date() else 'Не указана'
    print(f"ID: {client.get_id()}, {client.get_surname()} {client.get_firstname()}, "
          f"Email: {client.get_email() or 'Не указан'}, Баланс: {client.get_balance()}, "
          f"Дата рождения: {birth_date}")


def main():
    # Инициализация репозитория
    repo = Client_rep_json('clients_data.json')

    print_section("ДЕМОНСТРАЦИЯ РАБОТЫ Client_rep_json")

    # f. Добавление клиентов
    print_section("f. Добавление клиентов в репозиторий")

    clients_to_add = [
        Client(surname="Иванов", firstname="Иван", fathers_name="Иванович",
               birth_date="15.05.1990", phone_number="+79991234567",
               pasport="1234 567890", email="ivanov@mail.ru", balance=5000.0),

        Client(surname="Петров", firstname="Петр", fathers_name="Петрович",
               birth_date="20.08.1985", phone_number="+79992345678",
               pasport="2345 678901", email="petrov@mail.ru", balance=10000.0),

        Client(surname="Сидоров", firstname="Сидор", fathers_name="Сидорович",
               birth_date="10.12.1995", phone_number="+79993456789",
               pasport="3456 789012", email="sidorov@mail.ru", balance=7500.0),

        Client(surname="Алексеева", firstname="Анна", fathers_name="Алексеевна",
               birth_date="05.03.1992", phone_number="+79994567890",
               pasport="4567 890123", email="alekseeva@mail.ru", balance=12000.0),

        Client(surname="Морозов", firstname="Дмитрий", fathers_name="Викторович",
               birth_date="25.07.1988", phone_number="+79995678901",
               pasport="5678 901234", email="morozov@mail.ru", balance=8500.0),
    ]

    for client in clients_to_add:
        added_client = repo.add_client(client)
        print(f"Добавлен клиент с ID: {added_client.get_id()}")

    # i. Получить количество элементов
    print_section("i. Получение количества элементов")
    count = repo.get_count()
    print(f"Всего клиентов в репозитории: {count}")

    # a. Чтение всех значений
    print_section("a. Чтение всех значений из файла")
    all_clients = repo.read_all()
    print(f"Прочитано клиентов: {len(all_clients)}")
    for client in all_clients:
        print_client(client)

    # c. Получить объект по ID
    print_section("c. Получение объекта по ID (ID = 3)")
    client = repo.get_by_id(3)
    if client:
        print_client(client)
    else:
        print("Клиент не найден")

    # e. Сортировка по email
    print_section("e. Сортировка по email")
    repo.sort_by_email()
    print("Клиенты после сортировки по email:")
    for client in repo.read_all():
        print_client(client)

    # d. Получение k-й страницы по n элементов (краткая информация)
    print_section("d. Получение 1-й страницы по 2 элемента (короткая информация)")
    short_list = repo.get_k_n_short_list(k=1, n=2)
    print(f"Получено записей: {len(short_list)}")
    for idx, short_info in enumerate(short_list, 1):
        print(f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, "
              f"Email: {short_info[5] or 'Не указан'}")

    print_section("d. Получение 2-й страницы по 2 элемента")
    short_list = repo.get_k_n_short_list(k=2, n=2)
    print(f"Получено записей: {len(short_list)}")
    for idx, short_info in enumerate(short_list, 1):
        print(f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, "
              f"Email: {short_info[5] or 'Не указан'}")

    # g. Замена элемента по ID
    print_section("g. Замена клиента с ID = 2")
    new_client = Client(surname="Новиков", firstname="Николай", fathers_name="Николаевич",
                        birth_date="15.11.1987", phone_number="+79996666666",
                        pasport="6666 666666", email="novikov@mail.ru", balance=15000.0)

    if repo.replace_by_id(2, new_client):
        print("Клиент успешно заменен!")
        updated = repo.get_by_id(2)
        print_client(updated)
    else:
        print("Клиент с ID = 2 не найден")

    # h. Удаление элемента по ID
    print_section("h. Удаление клиента с ID = 4")
    if repo.delete_by_id(4):
        print("Клиент успешно удален!")
        print(f"Осталось клиентов: {repo.get_count()}")
    else:
        print("Клиент с ID = 4 не найден")

    # b. Запись всех значений в файл (автоматически выполняется при изменениях)
    print_section("b. Итоговое состояние (автоматически записано в файл)")
    print("Текущее состояние репозитория:")
    for client in repo.read_all():
        print_client(client)

    print_section("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print(f"\nДанные сохранены в файл: {repo.file_path}")


if __name__ == "__main__":
    main()
