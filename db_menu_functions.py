"""
Функции меню для работы с БД и декорированными репозиториями
"""

from travel_agency.Client import Client
from travel_agency.Client_rep_DB_adapter import Client_rep_DB_adapter
from travel_agency.Client_rep_decorator import (
    BalanceFilter,
    Client_rep_decorator,
    ClientSorter,
    EmailFilter,
    SurnameFilter,
)
from travel_agency.DBConnection import DBConnection


def print_separator():
    print("\n" + "=" * 100)


def print_section_title(title):
    print_separator()
    print(f"\n{title.upper()}")
    print_separator()


def print_success(message):
    print(f"\n✓ {message}")


def print_error(message):
    print(f"\n✗ ОШИБКА: {message}")


def configure_db_connection():
    """Настройка подключения к PostgreSQL (автоматически, без ввода)"""
    print_section_title("ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ")

    try:
        db = DBConnection()
        # Используем захардкоженные параметры из DBConnection
        db.connect()
        print_success("Подключение к БД успешно установлено")
        print(f"  База данных: {db._database}")
        print(f"  Хост: {db._host}:{db._port}")
        print(f"  Пользователь: {db._user}")
        return True
    except Exception as e:
        print_error(f"Ошибка подключения: {e}")
        print("  Убедитесь, что PostgreSQL запущен и БД 'travel_agency' создана")
        print("  Выполните: psql -U postgres -d travel_agency -f database_setup.sql")
        return False


def print_client_full(client):
    birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else "Не указана"
    print(f"  ID: {client.get_id()}")
    print(f"  Фамилия: {client.get_surname()}")
    print(f"  Имя: {client.get_firstname()}")
    print(f"  Отчество: {client.get_fathers_name() or 'Не указано'}")
    print(f"  Дата рождения: {birth_date_str}")
    if isinstance(client, Client):
        print(f"  Телефон: {client.get_phone_number() or 'Не указан'}")
        print(f"  Паспорт: {client.get_pasport() or 'Не указан'}")
        print(f"  Email: {client.get_email() or 'Не указан'}")
        print(f"  Баланс: {client.get_balance() or '0.00'}")


def get_db_repository_menu_choice():
    print_separator()
    print("\nРАБОТА С POSTGRESQL БАЗОЙ ДАННЫХ:")
    print("1. Просмотреть все записи")
    print("2. Получить запись по ID (get_by_id)")
    print("3. Получить список с пагинацией (get_k_n_short_list)")
    print("4. Добавить нового клиента (add_client)")
    print("5. Заменить клиента по ID (replace_by_id)")
    print("6. Удалить клиента по ID (delete_by_id)")
    print("7. Получить количество записей (get_count)")
    print("8. Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1-8): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            return choice
        print_error("Неверный выбор. Введите число от 1 до 8.")


def work_with_db_repository():
    print_section_title("РАБОТА С POSTGRESQL РЕПОЗИТОРИЕМ")

    repo = Client_rep_DB_adapter()

    while True:
        choice = get_db_repository_menu_choice()

        if choice == "1":
            # Просмотр всех записей
            print_section_title("ВСЕ ЗАПИСИ ИЗ БД")
            clients = repo.read_all()
            if not clients:
                print("\nБД пуста")
            else:
                print(f"\nВсего записей: {len(clients)}")
                for client in clients:
                    print_client_full(client)
                    print("-" * 80)

        elif choice == "2":
            # Получить по ID
            print_section_title("ПОЛУЧЕНИЕ ЗАПИСИ ПО ID")
            try:
                client_id = int(input("Введите ID клиента: ").strip())
                client = repo.get_by_id(client_id)
                if client:
                    print("\nНайденный клиент:")
                    print_client_full(client)
                else:
                    print_error(f"Клиент с ID {client_id} не найден")
            except ValueError:
                print_error("ID должен быть числом")

        elif choice == "3":
            # Пагинация
            print_section_title("ПОЛУЧЕНИЕ СПИСКА С ПАГИНАЦИЕЙ")
            try:
                k = int(input("Введите номер страницы (k): ").strip())
                n = int(input("Введите количество элементов на странице (n): ").strip())
                short_list = repo.get_k_n_short_list(k, n)

                if not short_list:
                    print(f"\nНет данных для страницы {k}")
                else:
                    print(f"\nСтраница {k} (по {n} элементов):")
                    for idx, short_info in enumerate(short_list, 1):
                        print(
                            f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, Email: {short_info[5] or 'Не указан'}"
                        )
            except ValueError:
                print_error("k и n должны быть числами")

        elif choice == "4":
            # Добавление
            print_section_title("ДОБАВЛЕНИЕ НОВОГО КЛИЕНТА")

            surname = input("Фамилия: ").strip()
            firstname = input("Имя: ").strip()
            fathers_name = input("Отчество: ").strip() or None
            birth_date = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
            phone_number = input("Номер телефона: ").strip()
            pasport = input("Паспорт (XXXX XXXXXX): ").strip()
            email = input("Email: ").strip() or None
            balance_input = input("Баланс: ").strip()

            try:
                balance = float(balance_input) if balance_input else None

                new_client = Client(
                    surname=surname,
                    firstname=firstname,
                    fathers_name=fathers_name,
                    birth_date=birth_date,
                    phone_number=phone_number,
                    pasport=pasport,
                    email=email,
                    balance=balance,
                )

                added = repo.add_client(new_client)
                print_success(f"Клиент успешно добавлен с ID: {added.get_id()}")
                print("\nДобавленный клиент:")
                print_client_full(added)

            except ValueError as e:
                print_error(f"Ошибка валидации: {e}")
            except Exception as e:
                print_error(f"Ошибка: {e}")

        elif choice == "5":
            # Замена
            print_section_title("ЗАМЕНА КЛИЕНТА ПО ID")

            try:
                client_id = int(input("Введите ID клиента для замены: ").strip())

                existing = repo.get_by_id(client_id)
                if not existing:
                    print_error(f"Клиент с ID {client_id} не найден")
                    continue

                print("\nТекущие данные клиента:")
                print_client_full(existing)

                print("\nВведите новые данные:")
                surname = input("Фамилия: ").strip()
                firstname = input("Имя: ").strip()
                fathers_name = input("Отчество: ").strip() or None
                birth_date = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()
                phone_number = input("Номер телефона: ").strip()
                pasport = input("Паспорт (XXXX XXXXXX): ").strip()
                email = input("Email: ").strip() or None
                balance_input = input("Баланс: ").strip()

                balance = float(balance_input) if balance_input else None

                new_client = Client(
                    surname=surname,
                    firstname=firstname,
                    fathers_name=fathers_name,
                    birth_date=birth_date,
                    phone_number=phone_number,
                    pasport=pasport,
                    email=email,
                    balance=balance,
                )

                if repo.replace_by_id(client_id, new_client):
                    print_success(f"Клиент с ID {client_id} успешно заменен")
                    print("\nОбновленные данные:")
                    print_client_full(repo.get_by_id(client_id))
                else:
                    print_error("Ошибка при замене")

            except ValueError as e:
                print_error(f"Ошибка: {e}")
            except Exception as e:
                print_error(f"Ошибка: {e}")

        elif choice == "6":
            # Удаление
            print_section_title("УДАЛЕНИЕ КЛИЕНТА ПО ID")

            try:
                client_id = int(input("Введите ID клиента для удаления: ").strip())

                existing = repo.get_by_id(client_id)
                if not existing:
                    print_error(f"Клиент с ID {client_id} не найден")
                    continue

                print("\nДанные клиента для удаления:")
                print_client_full(existing)

                confirm = input("\nВы уверены? (да/нет): ").strip().lower()
                if confirm in ["да", "yes", "y"]:
                    if repo.delete_by_id(client_id):
                        print_success(f"Клиент с ID {client_id} успешно удален")
                        print(f"Осталось записей: {repo.get_count()}")
                    else:
                        print_error("Ошибка при удалении")
                else:
                    print("Удаление отменено")

            except ValueError:
                print_error("ID должен быть числом")

        elif choice == "7":
            # Количество записей
            print_section_title("КОЛИЧЕСТВО ЗАПИСЕЙ")
            count = repo.get_count()
            print(f"\nВсего записей в БД: {count}")

        elif choice == "8":
            # Выход
            return "menu"


def get_decorated_repository_menu_choice():
    print_separator()
    print("\nРАБОТА С ДЕКОРИРОВАННЫМ РЕПОЗИТОРИЕМ:")
    print("1. Установить фильтр по балансу")
    print("2. Установить фильтр по email")
    print("3. Установить фильтр по фамилии")
    print("4. Установить сортировку")
    print("5. Просмотреть данные с фильтрами")
    print("6. Получить список с пагинацией (с фильтрами)")
    print("7. Получить количество (с учетом фильтров)")
    print("8. Очистить все фильтры и сортировку")
    print("9. Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1-9): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice
        print_error("Неверный выбор. Введите число от 1 до 9.")


def work_with_decorated_repository():
    print_section_title("РАБОТА С ДЕКОРИРОВАННЫМ РЕПОЗИТОРИЕМ")

    print("\nВыберите тип репозитория для декорирования:")
    print("1 - JSON репозиторий")
    print("2 - YAML репозиторий")
    print("3 - БД репозиторий")

    repo_choice = input("\nВаш выбор (1-3): ").strip()

    if repo_choice == "1":
        from travel_agency.Client_rep_json import Client_rep_json

        base_repo = Client_rep_json("clients_data.json")
        repo_name = "JSON"
    elif repo_choice == "2":
        from travel_agency.Client_rep_yaml import Client_rep_yaml

        base_repo = Client_rep_yaml("clients_data.yaml")
        repo_name = "YAML"
    elif repo_choice == "3":
        base_repo = Client_rep_DB_adapter()
        repo_name = "БД"
    else:
        print_error("Неверный выбор")
        return "menu"

    # Создаем декорированный репозиторий
    decorated_repo = Client_rep_decorator(base_repo)
    print_success(f"Декорированный {repo_name} репозиторий создан")

    while True:
        choice = get_decorated_repository_menu_choice()

        if choice == "1":
            # Фильтр по балансу
            print_section_title("ФИЛЬТР ПО БАЛАНСУ")
            min_bal = input("Минимальный баланс (Enter - без ограничения): ").strip()
            max_bal = input("Максимальный баланс (Enter - без ограничения): ").strip()

            min_balance = float(min_bal) if min_bal else None
            max_balance = float(max_bal) if max_bal else None

            decorated_repo.add_filter(BalanceFilter(min_balance, max_balance))
            print_success("Фильтр по балансу установлен")

        elif choice == "2":
            # Фильтр по email
            print_section_title("ФИЛЬТР ПО EMAIL")
            print("1 - Только с email")
            print("2 - Только без email")
            email_choice = input("\nВаш выбор (1-2): ").strip()

            if email_choice == "1":
                decorated_repo.add_filter(EmailFilter(has_email=True))
                print_success("Фильтр установлен: только клиенты с email")
            elif email_choice == "2":
                decorated_repo.add_filter(EmailFilter(has_email=False))
                print_success("Фильтр установлен: только клиенты без email")

        elif choice == "3":
            # Фильтр по фамилии
            print_section_title("ФИЛЬТР ПО ФАМИЛИИ")
            starts_with = input("Фамилия начинается с: ").strip()

            if starts_with:
                decorated_repo.add_filter(SurnameFilter(starts_with))
                print_success(f"Фильтр установлен: фамилия начинается с '{starts_with}'")

        elif choice == "4":
            # Сортировка
            print_section_title("УСТАНОВКА СОРТИРОВКИ")
            print("1 - По фамилии (возрастание)")
            print("2 - По фамилии (убывание)")
            print("3 - По балансу (возрастание)")
            print("4 - По балансу (убывание)")
            print("5 - По email (возрастание)")
            print("6 - По email (убывание)")

            sort_choice = input("\nВаш выбор (1-6): ").strip()

            if sort_choice == "1":
                decorated_repo.set_sorter(ClientSorter.by_surname(reverse=False))
                print_success("Сортировка: по фамилии (возрастание)")
            elif sort_choice == "2":
                decorated_repo.set_sorter(ClientSorter.by_surname(reverse=True))
                print_success("Сортировка: по фамилии (убывание)")
            elif sort_choice == "3":
                decorated_repo.set_sorter(ClientSorter.by_balance(reverse=False))
                print_success("Сортировка: по балансу (возрастание)")
            elif sort_choice == "4":
                decorated_repo.set_sorter(ClientSorter.by_balance(reverse=True))
                print_success("Сортировка: по балансу (убывание)")
            elif sort_choice == "5":
                decorated_repo.set_sorter(ClientSorter.by_email(reverse=False))
                print_success("Сортировка: по email (возрастание)")
            elif sort_choice == "6":
                decorated_repo.set_sorter(ClientSorter.by_email(reverse=True))
                print_success("Сортировка: по email (убывание)")

        elif choice == "5":
            # Просмотр с фильтрами
            print_section_title("ДАННЫЕ С ПРИМЕНЕНИЕМ ФИЛЬТРОВ И СОРТИРОВКИ")
            clients = decorated_repo.read_all()

            if not clients:
                print("\nНет данных, соответствующих фильтрам")
            else:
                print(f"\nНайдено записей: {len(clients)}")
                for client in clients:
                    print_client_full(client)
                    print("-" * 80)

        elif choice == "6":
            # Пагинация с фильтрами
            print_section_title("ПАГИНАЦИЯ С ФИЛЬТРАМИ")
            try:
                k = int(input("Номер страницы (k): ").strip())
                n = int(input("Элементов на странице (n): ").strip())

                short_list = decorated_repo.get_k_n_short_list(k, n)

                if not short_list:
                    print(f"\nНет данных для страницы {k}")
                else:
                    print(f"\nСтраница {k} (по {n} элементов):")
                    for idx, short_info in enumerate(short_list, 1):
                        print(
                            f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, Email: {short_info[5] or 'Не указан'}"
                        )
            except ValueError:
                print_error("k и n должны быть числами")

        elif choice == "7":
            # Количество с фильтрами
            print_section_title("КОЛИЧЕСТВО С УЧЕТОМ ФИЛЬТРОВ")
            count = decorated_repo.get_count()
            print(f"\nКоличество записей (с фильтрами): {count}")

        elif choice == "8":
            # Очистка фильтров
            decorated_repo.clear_filters()
            decorated_repo.clear_sorter()
            print_success("Все фильтры и сортировка очищены")

        elif choice == "9":
            # Выход
            return "menu"
