# Напишите декоратор @logger, который после выполнения
# функции напишет название функции и статус выполнения
# (если произошло исключение нужно вывести
# сообщение “exc_has_appeared”, иначе вывести только название функции.
from functools import wraps


def logger(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        print(func.__name__)
        try:
            func(*args, **kwargs)
        except ZeroDivisionError:
            print("ZeroDivisionError")
    return _wrapper


# Код для самопроверки
@logger
def function_with_error():
    var = 1/0
    return var


@logger
def working_function():
    pass


# Запустите этот файл для проверки
if __name__ == "__main__":
    # Вызов функции ниже должен вывести в терминал название функции
    # и сообщить, что произошла ошибка
    function_with_error()
    # Вызов функции ниже должен вывести только ее название
    working_function()
