import functools
from datetime import datetime, timezone
import string
import time
import logging


class AuthenticationError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class User:

    def __init__(self, name: str,
                 role: str,
                 logged_in: bool):
        self.name = name
        self.role = role
        self.logged_in = logged_in


def authenticate(func):
    def wrapper(self, user, *args, **kwargs):
        if not user.logged_in:
            raise AuthenticationError(f"Исключение. {user.name} не авторизован.")
        print(f"{user.name} Авторизирован")
        return func(self, user, *args, **kwargs)

    return wrapper


def authorize(role):
    def decorator(func):
        def wrapper(self, user, *args, **kwargs):
            if user.role != role:
                raise AuthorizationError(f"Исключение. {user.name} не является Админом.")
            print(f"{user.name} является админом")
            return func(self, user, *args, **kwargs)

        return wrapper

    return decorator


def log_operation(func):
    def wrapper(self, user, *args, **kwargs):
        utc_dt = datetime.now(timezone.utc).replace(microsecond=0)
        start_time = time.time()
        result = func(self, user, *args, **kwargs)
        end_time = time.time()
        file_log_operation = 'log_operation.txt'
        logs = [f"Вызываемая функция: {func.__name__}",
                f"Аргументы функции: {user.name}, {user.role}, {user.logged_in}",
                f"Результат функции: {result}",
                f"Начало работы функции: {utc_dt.strftime('%Y-%m-%d %H:%M:%S')}",
                f"Время работы функции: {end_time - start_time} секунд\n"]

        for log in logs:
            print(log)

        with open(f'{file_log_operation}', 'a', newline='', encoding='utf-8') as file:
            for log in logs:
                file.write(log + "\n")

        return result

    return wrapper


def cache_result(expire_time):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                result, timestamp = cache[args]
                if time.time() - timestamp < expire_time:
                    print('\nДанные из Кеша')
                    print(result)
                    return result
                else:
                    del cache[args]
            result = func(*args)
            cache[args] = (result, time.time())
            return result

        return wrapper

    return decorator


class System:
    @authenticate
    @log_operation
    def open_file(self, user):
        text = f"Пользователь {user.name} открыл файл."
        return text

    @authenticate
    @authorize("Админ")
    @log_operation
    def delete_file(self, user):
        text = f"Пользователь {user.name} удалил файл."
        return text

    @authorize("Админ")
    @authenticate
    @log_operation
    @cache_result(3)
    def copy_file(self, user):
        text = f"Пользователь {user.name} копировал файл."
        return text


admin = User("Мартим", "Админ", True)
guest_logged = User("Тим", "Гость", True)
guest_no_logged = User("Марс", "Гость", False)

system = System()

try:
    print(f'{system.open_file(admin)}\n')
except Exception as e:
    print(e)

try:
    print(f'{system.open_file(guest_logged)}\n')
except Exception as e:
    print(e)

try:
    print(f'{system.open_file(guest_no_logged)}\n')
except Exception as e:
    print(e)

try:
    print(f'{system.copy_file(admin)}\n')
except Exception as e:
    print(e)

time.sleep(2)

try:
    print(f'{system.copy_file(admin)}\n')
except Exception as e:
    print(e)

time.sleep(2)

try:
    print(f'{system.copy_file(admin)}\n')
except Exception as e:
    print(e)