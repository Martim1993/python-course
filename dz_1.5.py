contacts = []

while True:

    print("Меню:")
    print("1. Добавить контакт")
    print("2. Удалить контакт")
    print("3. Поиск контакта")
    print("4. Вывод всех контактов")
    print("5. Выход из программы\n")
    number = input("Выберите действие (1-5): ")

    if number.isdigit():
        number = int(number)

        if number in range(1,6):

            if number == 1:

                contacts_exsist = False
                print("\nВы выбрали: 1. Добавить контакт")
                print("Для сохранения контакта введите пожалуйста следующие данные\n")
                name = input("Ведите пожалуйста имя: ")
                surname = input("Ведите пожалуйста фамилию: ")
                phone = input("Ведите пожалуйста телефон: ")
                email = input("Ведите пожалуйста email: ")

                if contacts:

                    for contact in contacts:

                        if (contact['name'] == name and
                                contact['surname'] == surname and
                                contact['phone'] == phone and
                                contact['email'] == email):

                            contacts_exsist = True

                if contacts_exsist == True:

                    print(f"\nКонтакт с именем {name}, фамилией {surname}, "
                          f"телефоном {phone} и email {email} уже есть в контактной книге\n")

                else:

                    contacts.append({'name': name,
                                     'surname': surname,
                                     'phone': phone,
                                     'email': email})
                    print(f"\nКонтакт с именем {name}, фамилией {surname}, "
                          f"телефоном {phone} и email {email} успешно добавлен\n")

            if number == 2:

                print("\nВы выбрали: 2. Удалить контакт")
                print("Для удаления контакта введите пожалуйста имя и фамилию контакта\n")
                name_remove = input("Имя удаляемого контакта: ")
                surname_remove = input("Фамилия удаляемого контакта: ")
                found = False

                for contact in contacts:

                    if contact['name'] == name_remove and contact['surname'] == surname_remove:
                        print(f"\nКонтакт с именем {name_remove}, фамилией {surname_remove}, "
                              f"телефоном {contact['phone']} и email {contact['email']} успешно удален.\n")
                        contacts.remove(contact)
                        found = True

                if found == False:

                    print(f'\nКонтакт с именем {name_remove} и фамилией {surname_remove} не найден\n')

            if number == 3:

                print("\nВы выбрали: 3. Поиск контакта")
                print("Для поиска контакта введите пожалуйста имя и фамилию контакта\n")
                find_name = input("Имя контакта которого ищете: ")
                find_surname = input("Фамилия контакта которого ищете: ")

                found = False

                for contact in contacts:

                    if contact['name'] == find_name and contact['surname'] == find_surname:
                        print(f'\nНайден контакт:')
                        print(f"Имя: {{{contact['name']}}}")
                        print(f"Фамилия: {{{contact['surname']}}}")
                        print(f"Телефон: {{{contact['phone']}}}")
                        print(f"Email: {{{contact['email']}}}\n")
                        found = True

                if found == False:

                    print(f'\nКонтакт с именем {find_name} и фамилией {find_surname} не найден\n')

            if number == 4:

                print("\nВы выбрали: 4. Вывод всех контактов\n")

                for contact in contacts:

                    print(f"Имя: {{{contact['name']}}}")
                    print(f"Фамилия: {{{contact['surname']}}}")
                    print(f"Телефон: {{{contact['phone']}}}")
                    print(f"Email: {{{contact['email']}}}\n")

            if number == 5:

                print("\nВы выбрали: 5. Выход из программы\n")
                print("\nДосвидания")
                break

    else:

        print(f"\nВы ввели не верные данные, пожалуйста попробуйте ещё раз\n")





