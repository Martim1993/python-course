number1 = int(input("Введите первое целое число: "))
number2 = int(input("Введите второе целое число: "))
operation = input("Введите пожалуйста операцию: ")


if operation == "+":
    sum1 = number1 + number2
    print(sum1)

elif operation == "-":
    difference = number1 - number2
    print(difference)

elif operation == "/":
    if number2 == 0:
        print("На ноль делить нельзя!")
    else:
        division = number1 / number2
        print(division)

elif operation == "*":
    multiplication = number1 * number2
    print(multiplication)

elif operation == "**":
    exponentiation = number1 ** number2
    print(exponentiation)
else:
    print("Что-то пошло не так!")
