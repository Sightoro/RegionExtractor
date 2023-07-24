# чтение входного файла с записью адресов в лист
import re
import sqlite3
import argparse

alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


parser = argparse.ArgumentParser(description='dbf file for DB')
parser.add_argument('indir', type=str, help='Input dir for videos')
args = parser.parse_args()
name_of_dbf_file = args.indir

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
    ansi = []
    if arr_of_addr[arr_of_addr.index(word) + 1][0].isupper():
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
        index_flag = False
        for elem in full_adr:
            # проверяем на наличие индекса

            if re.fullmatch(r'\d{6}', str(elem)):

                cur.execute(
                    "SELECT region FROM {table} WHERE `index` LIKE \
                    {index}".format(table=name_of_dbf_file, index=str("'" + str(elem)[0:3] + "___\'")))
                ans = set(cur.fetchall())
                if index_flag and ans:
                    ans = []
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
if last_ans:
    for ans_region in set(last_ans):
        print(ans_region)
else:
    print("-1")
