import random


with open('russian.txt', 'r') as file:
    words = file.readlines()
    words = [s.strip("\n") for s in words]

secret_word = random.choice(words)
print(secret_word) # что бы знать какое загаданное слово
success_word = list(range(len(secret_word)))
attempts = 3
success_word_repead = list(range(len(secret_word)))


def input_one_letter(prompt):
    while True:
        user_input = input(prompt)

        if len(user_input) == 1 and user_input.isalpha():
            return user_input

        else:
            print("Пожалуйста, введите только одну букву.")


while attempts > 0:
    user_word = input_one_letter("Введите одну букву: ")
    num_secret_word = len(list(filter(lambda x: isinstance(x, str), success_word)))

    for i in range(len(secret_word)):
        if secret_word[i] == user_word:
            success_word[i] = secret_word[i]

    for j in success_word:
        if j == str(j):
            print(j, end='')
        else:
            print('*', end='')

    num_success_word = len(list(filter(lambda x: isinstance(x, str), success_word)))

    print(success_word_repead)
    if user_word in success_word_repead:
        print()
        print(f'Буква "{user_word}" уже отгаданна в слове!')

    elif success_word == list(secret_word):
        print()
        print('Поздравляю вы угадали слово')
        break

    elif attempts > 1:

        if num_secret_word == num_success_word:
            attempts -= 1
            print()
            print(f'Вы израсходовали одну попытку. Осталось {attempts} попыток')
        else:
            print()
            print(f'Вы отгадали одну букву. Осталось {attempts} попыток')

    else:
        print()
        print(f'Вы израсходовали все попытки. Засекреченное слово было: {secret_word}')
        break
    success_word_repead = set(success_word)
    print()

