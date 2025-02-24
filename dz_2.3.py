import random

word_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

print(f"Число из списка от 0 до 100: {random.choice(range(0, 101))}")

print(f"Число с плавающей точкой от 0 до 1: {random.random()}")

print(f"Число из списка от -50 до 50: {random.choice(range(-50, 50))}")

print(f"Созданный список: {word_list}")

print(f"Значение из списка: {random.choice(word_list)}")

random.shuffle(word_list)
print(f"Перемешанный список: {word_list}")

bone_1 = random.choice(range(1, 7))
bone_2 = random.choice(range(1, 7))
print(f"Сумма двух костей {bone_1 + bone_2}")

print(f"Три случайных значения без повторов: {random.sample(word_list, k=3)}")
