import random
import string
сycle = 0

def generate_password(password_len):

    symbols = '!@#$%^&*()-+'
    password_element = string.ascii_letters + string.digits + symbols
    password = ''.join(random.choice(password_element) for _ in range(int(password_len)))
    return password


while сycle == 0:

    print("Выберите действие:")
    print("1. Сгенерировать новый пароль")
    print("2. Проверить надежность пароля")
    print("3. Выход из программы\n")
    print("Для того что бы начать работу пожалуйста выберете действие: 1. Сгенерировать новый пароль")
    number = input("Введите номер действия: ")
    сycle += 1

    if int(number) == 1:

        password_len = input("Введите длину пароля: ")
        print(f'{generate_password(password_len)}\n')

    else:

        print("Вы сделали неправельный выбор.")

while сycle == 1:

    print("Выберите действие:")
    print("1. Сгенерировать новый пароль")
    print("2. Проверить надежность пароля")
    print("3. Выход из программы\n")
    number = input("Введите номер действия: ")

    if int(number) == 1:

        password_len = input("Введите длину пароля: ")
        print(f'{generate_password(password_len)}\n')

    elif int(number) == 2:

        password = input("Введите пароль для проверки: ")
        symbols = '!@#$%^&*()-+'
        password_element = string.ascii_letters + string.digits + symbols

        prohibited_password_element = set(password)

        if any(char not in password_element for char in prohibited_password_element):

            print('Ошибка. Запрещенный спецсимвол')

        else:

            recommendations = []

            if len(password) < 12:

                recommendations.append(f'увеличить число символов - {12 - len(password)}')

            for what, message in ((string.digits, 'цифру'),

                                  (symbols, 'спецсимвол'),

                                  (string.ascii_letters, 'заглавную или строчную букву ')):

                if all(char not in what for char in prohibited_password_element):

                    recommendations.append(f'добавить 1 {message}')

            if recommendations:

                print("Слабый пароль. Рекомендации:", ", ".join(recommendations),"\n")

            else:

                print('Сильный пароль.\n')

    elif int(number) == 3:

        print("Выход из программы")
        break