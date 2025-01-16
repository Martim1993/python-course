import string

word_max = ''
len_word_max = 0
words_max = 0
dictionary_word = {}

input_words_file = input(f"Введите пожалуста название файла: ")
words_file = open(f"{input_words_file}.txt", "r", encoding="utf-8")
words = words_file.readline()

for p in string.punctuation:
    if p in words:
        words = words.replace(p, '')

words = words.lower().split(" ")

for word in words:

    if len(word) > len_word_max:
        word_max = word
        len_word_max = len(word)

for word in words:

    if word in dictionary_word:
        dictionary_word[word] += 1

    else:
        dictionary_word[word] = 1

max_quantity_word = None
max_quantity = 0

for word, quantity in dictionary_word.items():

    if quantity > max_quantity:
        max_quantity = quantity
        max_quantity_word = word

word_count = f"Количество слов: {len(words)}"
number_of_unique_words = f"Количество уникальных слов: {len(set(words))}"
longest_word = f"Самое длинное слово: {word_max} (длина: {len_word_max})"
most_common_word = f"Самое частое слово: {max_quantity_word} (количество: {max_quantity})"

print(word_count)
print(number_of_unique_words)
print(longest_word)
print(most_common_word)

my_file = open(f"{input_words_file}_analysis.txt", "w+", encoding="utf-8")
my_file.write(f"{word_count}\n"
              f"{number_of_unique_words}\n"
              f"{longest_word}\n"
              f"{most_common_word}\n")
my_file.close()


