import string

text_1 = input("Введите пожалуйста текст №1: ")
text_2 = input("Введите пожалуйста текст №2: ")

if text_1 == '':
    print("\nВ Первом тексте отсутвует текст")

elif text_2 == '':
    print("\nВо Втором тексте отсутвует текст")

else:
    for p in string.punctuation:
        if p in text_1:
            text_1 = text_1.replace(p, '')
            text_1 = text_1.replace('— ', '')

    for p in string.punctuation:
        if p in text_2:
            text_2 = text_2.replace(p, '')
            text_2 = text_2.replace('— ', '')

    list_text_1 = text_1.split(' ')
    list_text_1 = set(list_text_1)
    list_text_2 = text_2.split(' ')
    list_text_2 = set(list_text_2)

    print(f"\nУникальные слова в тексте 1: {list_text_1}\n")
    print(f"Уникальные слова в тексте 2: {list_text_2}\n")
    print(f"Общие слова: {list_text_1 & list_text_2}\n")
    print(f"Слова из текста 1, отсутствующие в тексте 2: {list_text_1.difference(list_text_2)}\n")
    print(f"Слова из текста 2, отсутствующие в тексте 1: {list_text_2.difference(list_text_1)}\n")
    print(f"Слова, присутствующие только в одном из текстов: "
          f"{list_text_1.difference(list_text_2).union(list_text_2.difference(list_text_1))}")