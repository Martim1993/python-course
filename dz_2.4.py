num = int(input("Пожалуйста введите порядковое число Фибоначи: "))


def fib(n: int):
    count = 0
    a = 1
    b = 1
    while True:
        if count < n:
            count = count + 1
            a, b = b, a+b
            yield b
        else:
            break


fibonachi = fib(num)

for value in fibonachi:
    print(value)

