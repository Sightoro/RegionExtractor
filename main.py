import re
import sqlite3


alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


# словарь с наменованиями субъектов и их полными названиями
# для вывода в ответ
def read_obl_txt():
    with open("obl.txt", "r") as file1:
        dict_lvl = {a: a + " область" for a in
                    file1.read().split("\n")}
    return dict_lvl


def read_republic_txt():
    with open("republic.txt", "r") as file2:
        regions_names = [a.split(":") for a in file2.read().split("\n")]
    return regions_names


# чтение входных данных
def read_input_values():
    with open("in.txt", "r") as file:
        all_addresses = [re.split(r'\s*\W\s*', a) for a in
                         file.read().split('\n')]
        return all_addresses


# открытие бд
def open_db():
    con = sqlite3.connect("addresses_database.db")
    cur = con.cursor()
    return cur


# закрытие бд
def close_db(cur):
    cur.close()


dict_level = read_obl_txt()
list4levels = [["Ненецкий", "Ненецкий автономный округ"],
               ["Ханты", "Ханты-Мансийский"
                         " автономный округ - Югра"],
               ["Югра", "Ханты-Мансийский"
                        " автономный округ - Югра"],
               ["Мансийский", "Ханты-Мансийский"
                              " автономный округ - Югра"],
               ["Чукотский", "Чукотский автономный округ"],
               ["Ямало", "Ямало-Ненецкий автономный округ"],
               ["Ненецкий", "Ямало-Ненецкий автономный округ"],
               ["Еврейская", "Еврейская автономная область"],
               ["Москва", "Москва"],
               ["Санкт", "Санкт-Петербург"],
               ["Петербург", "Санкт-Петербург"],
               ["Севастополь", "Севастополь"],
               ["Алтайский", "Алтайский край"],
               ["Забайкальский", "Забайкальский край"],
               ["Камчатский", "Камчатский край"],
               ["Краснодарский", "Краснодарский край"],
               ["Красноярский", "Красноярский край"],
               ["Пермский", "Пермский край"],
               ["Приморский", "Приморский край"],
               ["Ставропольский", "Ставропольский край"],
               ["Хабаровский", "Хабаровский край"]]
for i in read_republic_txt():
    dict_level[i[0]] = i[1]
for i in list4levels:
    dict_level[i[0]] = i[1]

# создание словаря, в котором ключ - первая буква,
# а значение - название субъектаы
regions_dict = {a: [] for a in alphabet}
for region in dict_level.keys():
    regions_dict[region[0]].append(region)


# поиск субъектов в словаре по первой букве названия
def search_by_first_letter(word, letter_dict,
                           arr_of_addr, dict_addr):
    ansi = None
    try:
        if arr_of_addr[arr_of_addr.index(word)
                                + 1][0].isupper():
            for region_in_dict in \
                    letter_dict[
                        arr_of_addr[arr_of_addr.index(word) + 1][0]]:
                try:
                    if arr_of_addr[arr_of_addr.index(word) + 1][:-2] \
                            in region_in_dict and \
                            len(arr_of_addr[arr_of_addr.index(word) + 1][
                                :-2]) \
                            == len(region_in_dict) - 2:
                        ansi = dict_addr[region_in_dict]
                        return ansi

                except IndexError:
                    if arr_of_addr[
                        arr_of_addr.index(word) - 1] == "Народная" \
                            or arr_of_addr[arr_of_addr.index(word) - 1] \
                            == "народная":
                        if arr_of_addr[arr_of_addr.index(word) - 2][:-2] \
                                in region_in_dict and \
                                len(arr_of_addr[
                                        arr_of_addr.index(word) - 2][:-2]) \
                                == len(region_in_dict) - 2:
                            ansi = dict_addr[region_in_dict]
                            return ansi
                    if arr_of_addr[arr_of_addr.index(word) - 1][:-2] \
                            in region_in_dict and \
                            len(arr_of_addr[arr_of_addr.index(word) - 1][
                                :-2]) \
                            == len(region_in_dict) - 2:
                        ansi = dict_addr[region_in_dict]
                        return ansi
    except IndexError:
        try:
            if not ansi \
                    and arr_of_addr[arr_of_addr.index(word)
                                    - 1][0].isupper():
                for region_in_dict in \
                        letter_dict[arr_of_addr[arr_of_addr.index(word)
                                                - 1][0]]:
                    if arr_of_addr[arr_of_addr.index(word) - 1] \
                            == "Народная" \
                            or arr_of_addr[arr_of_addr.index(word) - 1] \
                            == "народная":
                        if arr_of_addr[arr_of_addr.index(word) - 2][:-2] \
                                in region_in_dict and \
                                len(arr_of_addr[
                                        arr_of_addr.index(word) - 2][:-2]) \
                                == len(region_in_dict) - 2:
                            ansi = dict_addr[region_in_dict]
                            return ansi
                    if arr_of_addr[arr_of_addr.index(word) - 1][:-2] \
                            in region_in_dict and \
                            len(arr_of_addr[arr_of_addr.index(word) - 1][
                                :-2]) \
                            == len(region_in_dict) - 2:
                        ansi = dict_addr[region_in_dict]
                        return ansi
        except IndexError or KeyError:
            return ansi
    try:
        if not ansi \
                and arr_of_addr[arr_of_addr.index(word)
                                - 1][0].isupper():
            for region_in_dict in \
                    letter_dict[arr_of_addr[arr_of_addr.index(word)
                                            - 1][0]]:
                if arr_of_addr[arr_of_addr.index(word) - 1] \
                        == "Народная" \
                        or arr_of_addr[arr_of_addr.index(word) - 1] \
                        == "народная":
                    if arr_of_addr[arr_of_addr.index(word) - 2][:-2] \
                            in region_in_dict and \
                            len(arr_of_addr[
                                    arr_of_addr.index(word) - 2][:-2]) \
                            == len(region_in_dict) - 2:
                        ansi = dict_addr[region_in_dict]
                        return ansi
                if arr_of_addr[arr_of_addr.index(word) - 1][:-2] \
                        in region_in_dict and \
                        len(arr_of_addr[arr_of_addr.index(word) - 1][
                            :-2]) \
                        == len(region_in_dict) - 2:
                    ansi = dict_addr[region_in_dict]
                    return ansi
    except IndexError or KeyError:
        return ansi


# функция проверяет, является ли город федерального значения
def is_it_federal_city(word, arr_of_addr):
    cities = [["Москва", "Москва"],
              ["Санкт-Петербург", "Санкт-Петербург"],
              ["Севастополь", "Севастополь"]]
    ansi = None
    for city in cities:
        try:
            if arr_of_addr[arr_of_addr.index(word) + 1] == city[0]:
                ansi = city[1]
                return ansi
        except IndexError:
            if arr_of_addr[arr_of_addr.index(word) - 1] == city[0]:
                ansi = city[1]
                return ansi
        try:
            if not ansi:
                for city in cities:
                    if arr_of_addr[arr_of_addr.index(word) - 1] == \
                            city[0]:
                        ansi = city[1]
                        return ansi
        except IndexError:
            break


# функция обработки строки выдающая на выходе найденый регион
def kochegar(my_address):
    cur = open_db()
    # перечесление всех возможных ключевых слов
    address_levels = [
        ["область", "обл", "Область", "о",
         "Автономный", "авт", "автономный", "а", "округ", "окр", "ао",
         "Край", "край", "кр",
         "Республика", "респ", "республика", "рес", "регион", "Регион",
         "рег", "р", "округ", "окр"],
        ["город", "г", "Город", "Г", "значения"]
    ]
    answer = []
    for full_adr in my_address:
        ans = None
        index_flag = False
        for elem in full_adr:
            # проверяем на наличие индекса

            if re.fullmatch(r'\d{6}', str(elem)):

                cur.execute(
                    "SELECT region FROM {table} WHERE `index` = \
                    {index}".format(table="address", index=str(
                        "'" + str(elem)[0:6] + "'")))
                ans = cur.fetchall()
                if ans:
                    tmp = ans[0][0]
                    tm = []
                    for i in tmp.split(" "):
                        if i:
                            tm.append(i)
                    ans = " ".join(tm)
                if index_flag and ans:
                    ans = None
                    continue
                index_flag = True
                if ans:
                    break
                else:
                    continue
            if elem in address_levels[1]:
                tmp_ans = is_it_federal_city(elem, full_adr)
                if tmp_ans:
                    ans = tmp_ans
                del tmp_ans
            if not ans and elem in address_levels[0]:
                tmp_ans = search_by_first_letter(elem, regions_dict,
                                                 full_adr, dict_level)
                if tmp_ans:
                    ans = tmp_ans
        if ans == "Республика Саха (Якутия)":
            print("______")
            print(full_adr)
            print("______")
        if ans:
            answer.append(ans)
    close_db(cur)
    if answer:
        for last_ans in set(answer):
            print(last_ans)
    else:
        print("-1")

    return set([a.lower() for a in answer])

op = [['683611', 'Курганская', 'область', 'Енисейск', 'ул.', 'Токарная', '64'], ['708133', 'Марий', 'Ессентуки', 'Аллея', 'Пуговишников', '734'], ['710892', 'Амурская', 'область', 'Осинники', 'Аллея', 'Лыковская', '569'], ['852061', 'Приморский', 'край', 'Строитель', 'ул.', 'Соломенной', 'Сторожки', '881'], ['756605', 'Воронежская', 'область', 'Учалы', 'ул.', 'Рассказовская', '813'], ['001862', 'Курганская', 'область', 'Заволжье', 'Аллея', 'Новомалино', '49'], ['641049', 'Кировская', 'область', 'Оренбург', 'Аллея', 'Дюссельдорфская', '227'], ['886916', 'Хакасия', 'Усмань', 'ул.', 'Налесная', '141'], ['460344', 'Алтай', 'Анадырь', 'Аллея', 'Долгопрудненское', '1324'], ['464613', 'Хабаровский', 'край', 'Верхний', 'Тагил', 'Аллея', 'Мукомольная', '227'], ['510950', 'Северная', 'Осетия', 'Злынка', 'Аллея', 'Тюрина', '604'], ['582190', 'Архангельская', 'область', 'Нытва', 'Аллея', 'Северная', '3-я', '267'], ['301736', 'Курская', 'область', 'Порхов', 'ул.', 'Циолковского', '4'], ['386474', 'Ивановская', 'область', 'Чусовой', 'ул.', 'Кирова', '522'], ['912308', 'Башкортостан', 'Осташков', 'ул.', 'Бунинская', 'Аллея', '297'], ['473887', 'Хабаровский', 'край', 'Кропоткин', 'Аллея', 'Молокова', '458'], ['570787', 'Чувашия', 'Дзержинский', 'Аллея', 'Канатчиковская', '1310'], ['085872', 'Ингушетия', 'Сычевка', 'Аллея', 'Шведская', '905'], ['561214', 'Владимирская', 'область', 'Топки', 'ул.', 'Звезд', 'Эстрады', '683'], ['031682', 'Приморский', 'край', 'Ельня', 'Аллея', 'Печорская', '1106'], ['776411', 'Липецкая', 'область', 'Ядрин', 'Аллея', 'Трехгорный', 'Б.', '33'], ['732363', 'Карелия', 'Хасавюрт', 'ул.', 'Хамовнический', 'Вал', '578'], ['749809', 'Белгородская', 'область', 'Отрадный', 'Аллея', 'Старопетровская', '723'], ['327049', 'Красноярский', 'край', 'Лысково', 'Аллея', 'Витебская', '356'], ['162790', 'Костромская', 'область', 'Чехов', 'Аллея', 'Моторная', '141'], ['337365', 'Удмуртия', 'Калининград', 'Аллея', 'Лестева', '1284'], ['221945', 'Татарстан', 'Талица', 'Аллея', 'Гамалеи', '56'], ['378851', 'Хакасия', 'Гусиноозёрск', 'ул.', 'Институтская', '2-я', '167'], ['963926', 'Красноярский', 'край', 'Саров', 'ул.', 'Сколковское', '115'], ['811598', 'Белгородская', 'область', 'Шарыпово', 'Аллея', 'Черниговская', '1145'], ['867160', 'Ленинградская', 'область', 'Киров', 'Аллея', 'Южнобутовская', '1235'], ['454289', 'Ивановская', 'область', 'Старый', 'Оскол', 'Аллея', 'Никитские', 'Ворота', '846'], ['043265', 'Чувашия', 'Октябрьск', 'ул.', 'Раушская', '455'], ['962878', 'Владимирская', 'область', 'Якутск', 'Аллея', 'Хибинская', '1251'], ['414197', 'Курганская', 'область', 'Пермь', 'Аллея', 'Молчановка', 'М.', '1102'], ['269607', 'Московская', 'область', 'Бузулук', 'Аллея', 'Прогонная', '1-я', '570'], ['298840', 'Воронежская', 'область', 'Нолинск', 'ул.', 'Стандартная', '696'], ['958201', 'Владимирская', 'область', 'Семикаракорск', 'Аллея', 'Велозаводская', '863'], ['481217', 'Удмуртия', 'Тобольск', 'Аллея', 'Марии', 'Ульяновой', '529'], ['299316', 'Воронежская', 'область', 'Мценск', 'Аллея', 'Краснопресненская', 'Застава', '208'], ['075994', 'Коми', 'Карпинск', 'Аллея', 'Станционная', '1034'], ['879919', 'Московская', 'область', 'Буй', 'Аллея', 'Осенняя', '429'], ['448410', 'Калмыкия', 'Козельск', 'ул.', 'Новокрымская', '551'], ['235435', 'Магаданская', 'область', 'Ялуторовск', 'ул.', 'Песочная', '108'], ['683570', 'Чечня', 'Дмитров', 'Аллея', 'Парковая', '3-я', '204'], ['750908', 'Владимирская', 'область', 'Чухлома', 'Аллея', 'Перовское', '361'], ['361180', 'Ставропольский', 'край', 'Алдан', 'ул.', 'Головановская', '910']]
kochegar(op)
last_ans = []
all_addresses = read_input_values()
#kochegar(all_addresses)


