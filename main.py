import json

from travel_agency.BaseClient import BaseClient
from travel_agency.Client import Client
from travel_agency.Client_rep_json import Client_rep_json
from travel_agency.Client_rep_yaml import Client_rep_yaml
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


def input_with_prompt(prompt, default=None):
    if default:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    else:
        return input(f"{prompt}: ").strip()


def get_continue_choice():
    print_separator()
    print("\nВыберите действие:")
    print("1 - Продолжить в текущем режиме")
    print("2 - Выбрать другой режим")
    print("3 - Просмотр всех созданных клиентов за сеанс")

    while True:
        choice = input("\nВаш выбор (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print_error("Неверный выбор. Введите 1, 2 или 3.")


def print_client_short(client):
    birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else "Не указана"
    print(f"  ID: {client.get_id()}")
    print(f"  Фамилия: {client.get_surname()}")
    print(f"  Имя: {client.get_firstname()}")
    print(f"  Отчество: {client.get_fathers_name() or 'Не указано'}")
    print(f"  Дата рождения: {birth_date_str}")
    if isinstance(client, Client):
        print(f"  Email: {client.get_email() or 'Не указан'}")


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


def is_client_unique(client, all_clients):
    return not any(existing_client == client for existing_client in all_clients)


def is_email_unique(email, all_clients):
    if not email or email.lower() in ["не указан", "none"]:
        return True
    client_count = 0
    for existing_client in all_clients:
        if isinstance(existing_client, Client) and existing_client.get_email():
            if existing_client.get_email().lower() == email.lower():
                client_count += 1
                if client_count >= 1:
                    return False
    return True


def delete_client_by_fio_and_birth_date(all_clients):
    if not all_clients:
        print("\nНет клиентов для удаления.")
        return False

    print("Введите данные клиента для удаления:")
    surname = input("Фамилия: ").strip()
    firstname = input("Имя: ").strip()
    fathers_name = input("Отчество (если нет - оставьте пустым): ").strip()
    birth_date_str = input("Дата рождения (ДД.ММ.ГГГГ): ").strip()

    try:
        from datetime import datetime

        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()

        # Нормализация введенных данных
        surname_norm = surname.lower().strip()
        firstname_norm = firstname.lower().strip()
        fathers_name_norm = fathers_name.lower().strip() if fathers_name else None
        if fathers_name_norm in ["", "не указано", "none"]:
            fathers_name_norm = None

        for i, client in enumerate(all_clients):
            # Нормализация данных клиента
            client_surname = client.get_surname().lower().strip()
            client_firstname = client.get_firstname().lower().strip()
            client_fathers_name = client.get_fathers_name()
            if client_fathers_name:
                client_fathers_name = client_fathers_name.lower().strip()
            else:
                client_fathers_name = None

            # Сравнение всех полей
            surname_match = client_surname == surname_norm
            firstname_match = client_firstname == firstname_norm

            # Гибкое сравнение отчества (оба None или оба равны)
            fathers_name_match = False
            if client_fathers_name is None and fathers_name_norm is None:
                fathers_name_match = True
            elif client_fathers_name is not None and fathers_name_norm is not None:
                fathers_name_match = client_fathers_name == fathers_name_norm
            elif client_fathers_name == "" and fathers_name_norm is None:
                fathers_name_match = True
            elif client_fathers_name is None and fathers_name_norm == "":
                fathers_name_match = True

            birth_date_match = client.get_birth_date() == birth_date

            if surname_match and firstname_match and fathers_name_match and birth_date_match:
                deleted_client = all_clients.pop(i)
                print_success(f"Клиент {deleted_client.get_surname()} {deleted_client.get_firstname()} удален!")
                return True

        print_error("Клиент с указанными ФИО и датой рождения не найден.")
        return False

    except ValueError as e:
        print_error(f"Ошибка ввода даты: {e}")
        return False


def display_clients_list(all_clients):
    if not all_clients:
        print("\nЗа текущий сеанс не было создано ни одного клиента.")
        return

    print(f"\nВсего создано клиентов: {len(all_clients)}")

    for i, client in enumerate(all_clients, 1):
        print(f"\n--- Клиент #{i} ---")
        if isinstance(client, Client):
            print_client_full(client)
        else:
            print_client_short(client)


def get_after_view_choice():
    print_separator()
    print("\nВыберите действие:")
    print("1 - Удалить клиента по ФИО и дате рождения")
    print("2 - Вернуться в главное меню")
    print("3 - Просмотр всех созданных клиентов за сеанс")

    while True:
        choice = input("\nВаш выбор (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print_error("Неверный выбор. Введите 1, 2 или 3.")


def get_after_delete_choice():
    print_separator()
    print("\nВыберите действие:")
    print("1 - Удалить ещё одного клиента по ФИО и дате рождения")
    print("2 - Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1-2): ").strip()
        if choice in ["1", "2"]:
            return choice
        print_error("Неверный выбор. Введите 1 или 2.")


def view_all_clients(all_clients):
    while True:
        print_section_title("ПРОСМОТР ВСЕХ СОЗДАННЫХ КЛИЕНТОВ ЗА СЕАНС")
        display_clients_list(all_clients)

        choice = get_after_view_choice()

        if choice == "1":
            if not all_clients:
                print("\nНет клиентов для удаления.")
                continue

            success = delete_client_by_fio_and_birth_date(all_clients)
            if success:
                print_section_title("ОБНОВЛЕННЫЙ СПИСОК КЛИЕНТОВ")
                display_clients_list(all_clients)

                after_delete_choice = get_after_delete_choice()
                if after_delete_choice == "1":
                    continue
                elif after_delete_choice == "2":
                    return "menu"

        elif choice == "2":
            return "menu"
        elif choice == "3":
            continue


def get_after_view_choice_simple():
    print_separator()
    print("\nВыберите действие:")
    print("1 - Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1): ").strip()
        if choice == "1":
            return choice
        print_error("Неверный выбор. Введите 1.")


def get_repository_menu_choice():
    print_separator()
    print("\nРАБОТА С JSON РЕПОЗИТОРИЕМ:")
    print("1. Просмотреть все записи (read_all)")
    print("2. Получить запись по ID (get_by_id)")
    print("3. Получить список с пагинацией (get_k_n_short_list)")
    print("4. Сортировать по email (sort_by_email)")
    print("5. Добавить нового клиента (add_client)")
    print("6. Заменить клиента по ID (replace_by_id)")
    print("7. Удалить клиента по ID (delete_by_id)")
    print("8. Получить количество записей (get_count)")
    print("9. Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1-9): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice
        print_error("Неверный выбор. Введите число от 1 до 9.")


def work_with_repository():
    print_section_title("РАБОТА С JSON РЕПОЗИТОРИЕМ")

    repo = Client_rep_json("clients_data.json")

    while True:
        choice = get_repository_menu_choice()

        if choice == "1":
            # Просмотр всех записей
            print_section_title("ВСЕ ЗАПИСИ ИЗ РЕПОЗИТОРИЯ")
            repo.reload_from_file()
            clients = repo.read_all()
            if not clients:
                print("\nРепозиторий пуст")
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
            # Сортировка
            print_section_title("СОРТИРОВКА ПО EMAIL")
            print("1 - По возрастанию")
            print("2 - По убыванию")
            sort_choice = input("\nВаш выбор (1-2): ").strip()

            if sort_choice == "1":
                repo.sort_by_email(reverse=False)
                print_success("Данные отсортированы по email (по возрастанию)")
            elif sort_choice == "2":
                repo.sort_by_email(reverse=True)
                print_success("Данные отсортированы по email (по убыванию)")
            else:
                print_error("Неверный выбор")
                continue

            print("\nОтсортированный список:")
            for client in repo.read_all():
                print(f"Email: {client.get_email() or 'Не указан'} - {client.get_surname()} {client.get_firstname()}")

        elif choice == "5":
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

        elif choice == "6":
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

        elif choice == "7":
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

        elif choice == "8":
            # Количество записей
            print_section_title("КОЛИЧЕСТВО ЗАПИСЕЙ")
            count = repo.get_count()
            print(f"\nВсего записей в репозитории: {count}")

        elif choice == "9":
            # Выход
            return "menu"


def get_yaml_repository_menu_choice():
    print_separator()
    print("\nРАБОТА С YAML РЕПОЗИТОРИЕМ:")
    print("1. Просмотреть все записи (read_all)")
    print("2. Получить запись по ID (get_by_id)")
    print("3. Получить список с пагинацией (get_k_n_short_list)")
    print("4. Сортировать по фамилии (sort_by_surname)")
    print("5. Добавить нового клиента (add_client)")
    print("6. Заменить клиента по ID (replace_by_id)")
    print("7. Удалить клиента по ID (delete_by_id)")
    print("8. Получить количество записей (get_count)")
    print("9. Вернуться в главное меню")

    while True:
        choice = input("\nВаш выбор (1-9): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice
        print_error("Неверный выбор. Введите число от 1 до 9.")


def work_with_yaml_repository():
    print_section_title("РАБОТА С YAML РЕПОЗИТОРИЕМ")

    repo = Client_rep_yaml("clients_data.yaml")

    while True:
        choice = get_yaml_repository_menu_choice()

        if choice == "1":
            # Просмотр всех записей
            print_section_title("ВСЕ ЗАПИСИ ИЗ YAML РЕПОЗИТОРИЯ")
            repo.reload_from_file()
            clients = repo.read_all()
            if not clients:
                print("\nРепозиторий пуст")
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
            # Сортировка
            print_section_title("СОРТИРОВКА ПО ФАМИЛИИ")
            print("1 - По возрастанию")
            print("2 - По убыванию")
            sort_choice = input("\nВаш выбор (1-2): ").strip()

            if sort_choice == "1":
                repo.sort_by_surname(reverse=False)
                print_success("Данные отсортированы по фамилии (по возрастанию)")
            elif sort_choice == "2":
                repo.sort_by_surname(reverse=True)
                print_success("Данные отсортированы по фамилии (по убыванию)")
            else:
                print_error("Неверный выбор")
                continue

            print("\nОтсортированный список:")
            for client in repo.read_all():
                print(f"{client.get_surname()} {client.get_firstname()} - Email: {client.get_email() or 'Не указан'}")

        elif choice == "5":
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

        elif choice == "6":
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

        elif choice == "7":
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

        elif choice == "8":
            # Количество записей
            print_section_title("КОЛИЧЕСТВО ЗАПИСЕЙ")
            count = repo.get_count()
            print(f"\nВсего записей в репозитории: {count}")

        elif choice == "9":
            # Выход
            return "menu"


def create_client_short_info_manual(all_clients):
    print_section_title("СОЗДАНИЕ КЛИЕНТА (КРАТКАЯ ИНФОРМАЦИЯ)")

    clients = []
    client_count = 0

    while True:
        client_count += 1
        print(f"\n--- Клиент #{client_count} ---")
        print("Введите данные или '0' для завершения:")

        surname = input_with_prompt("Фамилия")
        if surname == "0":
            break

        firstname = input_with_prompt("Имя")
        if firstname == "0":
            break

        fathers_name = input_with_prompt("Отчество")
        if fathers_name == "0":
            break
        fathers_name = None if fathers_name.lower() in ["не указано", "none"] else fathers_name

        birth_date = input_with_prompt("Дата рождения (ДД.ММ.ГГГГ)")
        if birth_date == "0":
            break
        birth_date = None if birth_date.lower() in ["не указано", "none"] else birth_date

        try:
            client = BaseClient(surname=surname, firstname=firstname, fathers_name=fathers_name, birth_date=birth_date)

            if not is_client_unique(client, all_clients):
                print_error("Клиент с такими ФИО и датой рождения уже существует!")
                continue

            clients.append(client)
            all_clients.append(client)
            print_success("Клиент успешно создан!")
            print("\nСозданный клиент:")
            print_client_short(client)

        except ValueError as e:
            print_error(str(e))
            continue
        except Exception as e:
            print_error(f"Неожиданная ошибка: {e}")
            continue

        choice = get_continue_choice()
        if choice == "1":
            continue
        elif choice == "2":
            return clients, "change_mode"
        elif choice == "3":
            result = view_all_clients(all_clients)
            if result == "menu":
                return clients, "change_mode"

    return clients, "continue"


def create_client_full_manual(all_clients):
    print_section_title("СОЗДАНИЕ КЛИЕНТА (ПОЛНАЯ ИНФОРМАЦИЯ)")

    clients = []
    client_count = 0

    while True:
        client_count += 1
        print(f"\n--- Клиент #{client_count} ---")
        print("Введите данные или '0' для завершения:")

        surname = input_with_prompt("Фамилия")
        if surname == "0":
            break

        firstname = input_with_prompt("Имя")
        if firstname == "0":
            break

        fathers_name = input_with_prompt("Отчество")
        if fathers_name == "0":
            break
        fathers_name = None if fathers_name.lower() in ["не указано", "none"] else fathers_name

        birth_date = input_with_prompt("Дата рождения (ДД.ММ.ГГГГ)")
        if birth_date == "0":
            break
        birth_date = None if birth_date.lower() in ["не указано", "none"] else birth_date

        phone_number = input_with_prompt("Номер телефона")
        if phone_number == "0":
            break

        pasport = input_with_prompt("Паспортные данные (XXXX XXXXXX)")
        if pasport == "0":
            break

        email = input_with_prompt("Email")
        if email == "0":
            break
        email = None if email.lower() in ["не указан", "none"] else email

        if email and not is_email_unique(email, all_clients):
            print_error("Клиент с таким email уже существует!")
            continue

        balance_input = input_with_prompt("Баланс")
        if balance_input == "0":
            break
        balance = None if balance_input.lower() in ["не указано", "none"] else balance_input

        try:
            balance_value = float(balance) if balance and balance.lower() not in ["не указано", "none"] else None

            client = Client(
                surname=surname,
                firstname=firstname,
                fathers_name=fathers_name,
                birth_date=birth_date,
                phone_number=phone_number,
                pasport=pasport,
                email=email,
                balance=balance_value,
            )

            if not is_client_unique(client, all_clients):
                print_error("Клиент с такими ФИО и датой рождения уже существует!")
                continue

            clients.append(client)
            all_clients.append(client)
            print_success("Клиент успешно создан!")
            print("\nСозданный клиент:")
            print_client_full(client)

        except ValueError as e:
            print_error(str(e))
            continue
        except Exception as e:
            print_error(f"Неожиданная ошибка: {e}")
            continue

        choice = get_continue_choice()
        if choice == "1":
            continue
        elif choice == "2":
            return clients, "change_mode"
        elif choice == "3":
            result = view_all_clients(all_clients)
            if result == "menu":
                return clients, "change_mode"

    return clients, "continue"


def json_conversion_test(all_clients):
    print_section_title("ТЕСТИРОВАНИЕ JSON КОНВЕРТАЦИИ")

    if not all_clients:
        print("Нет клиентов для тестирования JSON конвертации.")
        return "continue"

    print("Выберите клиента для тестирования JSON конвертации:")
    for i, client in enumerate(all_clients, 1):
        birth_info = f", {client.get_birth_date().strftime('%d.%m.%Y')}" if client.get_birth_date() else ""
        client_type = "Client" if isinstance(client, Client) else "BaseClient"
        print(f"{i}. {client.get_surname()} {client.get_firstname()}{birth_info} ({client_type})")

    try:
        choice = int(input("\nВведите номер клиента: ")) - 1
        if choice < 0 or choice >= len(all_clients):
            print_error("Неверный выбор клиента.")
            return "continue"
    except ValueError:
        print_error("Введите корректный номер.")
        return "continue"

    client = all_clients[choice]

    try:
        birth_date_str = client.get_birth_date().strftime("%d.%m.%Y") if client.get_birth_date() else None
        json_data = {
            "id": client.get_id(),
            "surname": client.get_surname(),
            "firstname": client.get_firstname(),
            "fathers_name": client.get_fathers_name(),
            "birth_date": birth_date_str,
        }

        if isinstance(client, Client):
            json_data.update(
                {
                    "phone_number": client.get_phone_number(),
                    "pasport": client.get_pasport(),
                    "email": client.get_email(),
                    "balance": client.get_balance(),
                }
            )

        json_str = json.dumps(json_data, ensure_ascii=False, indent=2)

        print("\nJSON данные:")
        print(json_str)

        if isinstance(client, Client):
            client_from_json = Client.from_json(json_str)
        else:
            client_from_json = BaseClient.from_json(json_str)

        print_success("Конвертация выполнена успешно!")
        print("\nКлиент из JSON:")
        if isinstance(client_from_json, Client):
            print_client_full(client_from_json)
        else:
            print_client_short(client_from_json)

        if client == client_from_json:
            print_success("Объекты равны!")
        else:
            print_error("Объекты не равны!")

    except Exception as e:
        print_error(f"Ошибка при конвертации: {e}")

    return get_after_view_choice_simple()


def string_conversion_manual(all_clients):
    print_section_title("ТЕСТИРОВАНИЕ FROM_STRING МЕТОДА")

    clients_created = []

    print("\nФормат данных: surname,firstname,fathers_name,birth_date,phone_number,pasport,email,balance")
    print("Пример: Петров,Иван,Иванович,15.05.1990,+79991234567,1234 567890,ivan@mail.ru,1000.50")
    print("Перечислите поля через запятую. Для пропуска полей используйте 'None'")

    while True:
        print_separator()
        string_input = input("\nВведите строку с данными (или '0' для выхода): ").strip()
        if string_input == "0":
            break

        if not string_input:
            print_error("Строка не может быть пустой")
            continue

        try:
            client = Client.from_string(string_input)

            if not is_client_unique(client, all_clients):
                print_error("Клиент с такими ФИО и датой рождения уже существует!")
                continue

            if client.get_email() and not is_email_unique(client.get_email(), all_clients):
                print_error("Клиент с таким email уже существует!")
                continue

            clients_created.append(client)
            all_clients.append(client)
            print_success("Клиент успешно создан из строки!")
            print("\nСозданный клиент:")
            print_client_full(client)

        except ValueError as e:
            print_error(f"Ошибка валидации: {e}")
        except Exception as e:
            print_error(f"Неожиданная ошибка: {e}")

        choice = get_continue_choice()
        if choice == "1":
            continue
        elif choice == "2":
            return "change_mode"
        elif choice == "3":
            result = view_all_clients(all_clients)
            if result == "menu":
                return "change_mode"

    return "continue"


def configure_db_connection():
    """Настройка подключения к PostgreSQL (автоматически, без ввода)"""
    print_section_title("ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ")

    try:
        db = DBConnection()
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
                        print(f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, Email: {short_info[5] or 'Не указан'}")
            except ValueError:
                print_error("k и n должны быть числами")

        elif choice == "4":
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
            print_section_title("КОЛИЧЕСТВО ЗАПИСЕЙ")
            count = repo.get_count()
            print(f"\nВсего записей в БД: {count}")

        elif choice == "8":
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
        base_repo = Client_rep_json("clients_data.json")
        repo_name = "JSON"
    elif repo_choice == "2":
        base_repo = Client_rep_yaml("clients_data.yaml")
        repo_name = "YAML"
    elif repo_choice == "3":
        base_repo = Client_rep_DB_adapter()
        repo_name = "БД"
    else:
        print_error("Неверный выбор")
        return "menu"

    decorated_repo = Client_rep_decorator(base_repo)
    print_success(f"Декорированный {repo_name} репозиторий создан")

    while True:
        choice = get_decorated_repository_menu_choice()

        if choice == "1":
            print_section_title("ФИЛЬТР ПО БАЛАНСУ")
            min_bal = input("Минимальный баланс (Enter - без ограничения): ").strip()
            max_bal = input("Максимальный баланс (Enter - без ограничения): ").strip()

            min_balance = float(min_bal) if min_bal else None
            max_balance = float(max_bal) if max_bal else None

            decorated_repo.add_filter(BalanceFilter(min_balance, max_balance))
            print_success("Фильтр по балансу установлен")

        elif choice == "2":
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
            print_section_title("ФИЛЬТР ПО ФАМИЛИИ")
            starts_with = input("Фамилия начинается с: ").strip()

            if starts_with:
                decorated_repo.add_filter(SurnameFilter(starts_with))
                print_success(f"Фильтр установлен: фамилия начинается с '{starts_with}'")

        elif choice == "4":
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
                        print(f"{idx}. ID: {short_info[0]}, {short_info[1]} {short_info[2]}, Email: {short_info[5] or 'Не указан'}")
            except ValueError:
                print_error("k и n должны быть числами")

        elif choice == "7":
            print_section_title("КОЛИЧЕСТВО С УЧЕТОМ ФИЛЬТРОВ")
            count = decorated_repo.get_count()
            print(f"\nКоличество записей (с фильтрами): {count}")

        elif choice == "8":
            decorated_repo.clear_filters()
            decorated_repo.clear_sorter()
            print_success("Все фильтры и сортировка очищены")

        elif choice == "9":
            return "menu"


def get_main_menu_choice():
    print_separator()
    print("\nВЫБЕРИТЕ РЕЖИМ РАБОТЫ:")
    print("1. Создание BaseClient (краткая информация)")
    print("2. Создание Client (полная информация)")
    print("3. Тестирование from_string метода")
    print("4. Тестирование from_json метода")
    print("5. Просмотр всех созданных клиентов за сеанс")
    print("6. Работа с JSON репозиторием (Client_rep_json)")
    print("7. Работа с YAML репозиторием (Client_rep_yaml)")
    print("8. Работа с PostgreSQL БД (Client_rep_DB)")
    print("9. Работа с декорированным репозиторием (фильтры и сортировка)")

    while True:
        choice = input("\nВаш выбор (1-9): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return choice
        print_error("Неверный выбор. Введите число от 1 до 9.")


def main():
    print_section_title("ПРОГРАММА ДЛЯ ТЕСТИРОВАНИЯ КЛАССОВ ТУРИСТИЧЕСКОЙ КОМПАНИИ")
    print("\nВведите '0' в любое поле для завершения ввода")

    all_clients = []

    while True:
        choice = get_main_menu_choice()

        if choice == "1":
            clients, status = create_client_short_info_manual(all_clients)
            if clients:
                print(f"\nИтого создано клиентов: {len(clients)}")
                for i, client in enumerate(clients, 1):
                    birth_info = f", {client.get_birth_date().strftime('%d.%m.%Y')}" if client.get_birth_date() else ""
                    print(f"{i}. {client.get_surname()} {client.get_firstname()}{birth_info} (ID: {client.get_id()})")
            if status == "change_mode":
                continue

        elif choice == "2":
            clients, status = create_client_full_manual(all_clients)
            if clients:
                print(f"\nИтого создано клиентов: {len(clients)}")
                for i, client in enumerate(clients, 1):
                    birth_info = f", {client.get_birth_date().strftime('%d.%m.%Y')}" if client.get_birth_date() else ""
                    print(f"{i}. {client.get_surname()} {client.get_firstname()}{birth_info} (ID: {client.get_id()})")
            if status == "change_mode":
                continue

        elif choice == "3":
            status = string_conversion_manual(all_clients)
            if status == "change_mode":
                continue

        elif choice == "4":
            status = json_conversion_test(all_clients)
            if status == "1":
                continue

        elif choice == "5":
            result = view_all_clients(all_clients)
            if result == "menu":
                continue

        elif choice == "6":
            status = work_with_repository()
            if status == "menu":
                continue

        elif choice == "7":
            status = work_with_yaml_repository()
            if status == "menu":
                continue

        elif choice == "8":
            # Настройка и работа с БД
            if configure_db_connection():
                status = work_with_db_repository()
                if status == "menu":
                    continue

        elif choice == "9":
            # Работа с декорированным репозиторием
            status = work_with_decorated_repository()
            if status == "menu":
                continue

    print_section_title("РАБОТА ПРОГРАММЫ ЗАВЕРШЕНА")


if __name__ == "__main__":
    main()
