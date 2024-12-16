import random


with open('russian.txt', 'r') as file:
    words = file.readlines()
    words = [s.strip("\n") for s in words]

secret_word = random.choice(words)
print(secret_word)
success_word = list(range(len(secret_word)))
attempts = 15


def input_one_letter(prompt):
    while True:
        user_input = input(prompt)
        if len(user_input) == 1 and user_input.isalpha():
            return user_input
        else:
            print("Пожалуйста, введите только одну букву.")


while attempts > 0:
    user_word = input_one_letter("Введите одну букву: ")

    for i in range(len(secret_word)):
        if secret_word[i] == user_word:
            success_word[i] = secret_word[i]

    for j in success_word:
        if j == str(j):
            print(j, end='')
        else:
            print('*', end='')

    if success_word == list(secret_word):
        print()
        print('Поздравляю вы угадали слово')
        break
    elif attempts > 1:
        attempts -= 1
        print()
        print(f'Вы израсходовали одну попытку. Осталось {attempts} попыток')
    else:
        print()
        print(f'Вы израсходовали все попытки. Засекреченное слово было: {secret_word}')
        break
    print()

