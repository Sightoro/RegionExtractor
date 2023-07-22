# чтение входного файла с записью адресов в лист
import re
import sqlite3


def vocabulary_lib():
    with open("input.txt", "r") as file:
        regions_names = file.readline().split(',')
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    region_dict_letter = {a: [] for a in alphabet}

    for name in regions_names:
        tmp_region = name.split()
        for tmp_word in tmp_region:
            if tmp_word[0] in region_dict_letter.keys() \
                    and not (name in region_dict_letter[tmp_word[0]]):
                region_dict_letter[tmp_word[0]].append(name.strip())
    return region_dict_letter
region_dict_letter = vocabulary_lib()


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


def read_all_regions():
    with open("input.txt", "r") as file3:
        return file3.readline().split(',')



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
               ["Ханты-Мансийский-Югра", "Ханты-Мансийский"
                                         " автономный округ - Югра"],
               ["Чукотский", "Чукотский автономный округ"],
               ["Ямало-Ненецкий", "Ямало-Ненецкий автономный округ"],
               ["Еврейская", "Еврейская автономная область"],
               ["Москва", "Москва"],
               ["Санкт-Петербург", "Санкт-Петербург"],
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
alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
regions_dict = {a: [] for a in alphabet}
regions = read_all_regions()
for region in regions:
    tmp_reg = region.split()
    for tmp_name in tmp_reg:

        if tmp_name[0] in regions_dict.keys() and not \
                (region in regions_dict[tmp_name[0]]):
            regions_dict[tmp_name[0]].append(region.strip())


# поиск субъектов в словаре по первой букве названия
def search_by_first_letter(word, letter_dict,
                           arr_of_addr, dict_addr):
    ansi = []
    for region_in_dict in \
            letter_dict[arr_of_addr[arr_of_addr.index(word) + 1][0]]:
        try:
            if arr_of_addr[arr_of_addr.index(word) + 1][:-2]\
                    in region_in_dict:
                ansi = dict_addr[region_in_dict]
                return ansi

        except IndexError:
            if arr_of_addr[arr_of_addr.index(word) - 1] == "Народная" \
                    or arr_of_addr[arr_of_addr.index(word) - 1] \
                    == "народная":
                if arr_of_addr[arr_of_addr.index(word) - 2][:-2]\
                        in region_in_dict:
                    ansi = dict_addr[region_in_dict]
                    return ansi
            if arr_of_addr[arr_of_addr.index(word) - 1][:-2]\
                    in region_in_dict:
                ansi = dict_addr[region_in_dict]
                return ansi
        try:
            if not ansi:
                for region_in_dict in \
                        letter_dict[arr_of_addr[arr_of_addr.index(word)
                                                + 1][0]]:
                    if arr_of_addr[arr_of_addr.index(word) - 1]\
                            == "Народная" \
                            or arr_of_addr[arr_of_addr.index(word) - 1]\
                            == "народная":
                        if arr_of_addr[arr_of_addr.index(word) - 2][:-2]\
                                in region_in_dict:
                            ansi = dict_addr[region_in_dict]
                            return ansi
                    if arr_of_addr[arr_of_addr.index(word) - 1][:-2]\
                            in region_in_dict:
                        ansi = dict_addr[region_in_dict]
                        return ansi
        except IndexError:
            break


# функция проверяет, является ли город федерального значения
def is_it_federal_city(word, arr_of_addr):
    cities = [["Москва", "Москва"],
                ["Санкт-Петербург", "Санкт-Петербург"],
                ["Севастополь", "Севастополь"]]
    ansi = []
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
         "рег", "р",
         "округ", "окр"],
        ["город", "г", "Город", "Г", "значения"],
        ["пос\.", "поселение", "р-н", "район", "с\/с", "сельсовет"],
        ["г", "город", "пгт", "рп", "кп\.", "гп\.", "п\.", "поселок",
         "аал", "арбан", "аул", "в-ки", "выселки",
         "г-к", "заимка", "з-ка", "починок", "п-к", "киш\.", "кишлак",
         "п\.ст\.", "ж\/д", "м-ко", "местечко", "деревня",
         "с\.", "село", "сл\.", "ст\.", "станция", "ст-ца", "станица",
         "у\.", "улус", "х\.", "хутор", "рзд\.",
         "разъезд", "зим\.", "зимовье", "д\."],
    ]
    answer = []
    for full_adr in my_address:
        ans = []
        for elem in full_adr:
            # проверяем на наличие индекса
            if re.fullmatch(r'\d{6}', str(elem)):
                cur.execute(
                    "SELECT region FROM PIndx01 WHERE `index` LIKE \
                    {}".format(str("'" + str(elem)[0:3] + "___\'")))
                ans = set(cur.fetchall())
                if ans:
                    break
                else:
                    continue
            if elem in address_levels[1]:
                ans = is_it_federal_city(elem, full_adr)
            if not ans and elem in address_levels[0]:
                ans = search_by_first_letter(elem, regions_dict,
                                             full_adr, dict_level)
        answer.append(ans)
    close_db(cur)
    return answer


last_ans = []
all_addresses = read_input_values()
for ans_region in kochegar(all_addresses):
    if type(ans_region) == str:
        last_ans.append(ans_region)
        continue
    if ans_region:
        last_ans.append(list(ans_region)[0][0].strip())

for ans_region in set(last_ans):
    print(ans_region)
