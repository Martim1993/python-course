data = "Иван Иванов: 5, 4, 3, 5, 2; Мария Петрова: 3, 3, 4, 2, 3; Петр Сидоров: 5, 5, 5, 5, 5; Анна Кузнецова: 4, 4, 4, 4, 4"
list_data = data.split(";")
name_average_value = ""
min_score = float('inf')
min_name = ""
max_score = float()
max_name = ""

for char in list_data:
    name = ""
    count = 0
    summa = 0

    for word in char:

        if word.isdigit():
            count += 1
            summa += int(word)
            average_value = summa/count

        if word.isalpha():
            name += word

        if word == " ":
            name += " "

    name_average_value += f"{name.strip()}: {average_value};"
    print(f"{name.strip()}: {average_value}")

name_average_value = name_average_value.split(';')

del name_average_value[4]

for entry in name_average_value:
    name, score = entry.split(': ')
    score = float(score)

    if score > max_score:
        max_score = score
        max_name = name

print(f'Студенты с максимальной средней оценкой: \n'
      f'{max_name}: Средняя оценка {max_score}\n')

for entry in name_average_value:
    name, score = entry.split(': ')
    score = float(score)

    if score < min_score:
        min_score = score
        min_name = name

print(f'Студенты с минимальной средней оценкой: \n'
      f'{min_name}: Средняя оценка {min_score}\n')

print(f'Студенты с низкой средней оценкой (< 4.0): \n')

for entry in name_average_value:
    name, score = entry.split(': ')
    score = float(score)

    if score < 4:
        print(f'{name}: Средняя оценка {score}')







