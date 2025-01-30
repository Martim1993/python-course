input_list = input('Вход: ')
input_list = list(input_list)


def find_max_recursive(lst):
    if len(lst) == 1:
        return lst[0]

    max_element = find_max_recursive(lst[1:])

    if lst[0] > max_element:
        return lst[0]

    else:
        return max_element


if input_list == []:
    print('Ваш список пустой. Введите пожалуйста список чисел')

else:
    print(f'Выход: {find_max_recursive(input_list)}')




