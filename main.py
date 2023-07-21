# чтение входного файла с записью адресов в лист
import re
import sqlite3


# словарь с наменованиями субъектов и их полными названиями
# для вывода в ответ
def read_obl_txt():
    with open("obl.txt", "r") as file1:
        dict_lvl = {0: [[a, a + " область"] for a in
                        file1.read().split("\n")]}
    return dict_lvl


def read_republic_txt():
    with open("republic.txt", "r") as file2:
        regions_names = [a.split(":") for a in file2.read().split("\n")]
    return regions_names


def read_all_regions():
    with open("input.txt", "r") as file3:
        regions = file3.readline().split(',')
        full_reg_name = file3.readline().split(',')
        fin = []
        region_id = 1
        for reg in regions:
            fin.append([region_id, str(reg).strip()])
            region_id += 1
    return full_reg_name, regions


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
dict_level[1] = [["Ненецкий", "Ненецкий автономный округ"],
                 ["Ханты-Мансийский", "Ханты-Мансийский автономный \
                        округ - Югра"],
                 ["Чукотский", "Чукотский автономный округ"],
                 ["Ямало-Ненецкий", "Ямало-Ненецкий автономный округ"],
                 ["Еврейская", "Еврейская автономная область"]]
dict_level[2] = [["Москва", "Москва"],
                 ["Санкт-Петербург", "Санкт-Петербург"],
                 ["Севастополь", "Севастополь"]]
dict_level[3] = [["Алтайский", "Алтайский край"],
                 ["Забайкальский", "Забайкальский край"],
                 ["Камчатский", "Камчатский край"],
                 ["Краснодарский", "Краснодарский край"],
                 ["Красноярский", "Красноярский край"],
                 ["Пермский", "Пермский край"],
                 ["Приморский", "Приморский край"],
                 ["Ставропольский", "Ставропольский край"],
                 ["Хабаровский", "Хабаровский край"]]
dict_level[4] = read_republic_txt()

# создание словаря, в котором ключ - первая буква,
# а значение - название субъектаы
alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
regions_dict = {a: [] for a in alphabet}
full_reg_name, regions = read_all_regions()
for region in regions:
    tmp_reg = region.split()
    for tmp_name in tmp_reg:

        if tmp_name[0] in regions_dict.keys() and not \
                (region in regions_dict[tmp_name[0]]):
            regions_dict[tmp_name[0]].append(region.strip())


# функция для поиска по наименованию субъекта
def search_by_level(iter_num, word, arr_of_levels,
                    arr_of_addr, dict_addr):
    ansi = []
    if word in arr_of_levels[iter_num]:
        for region_list in dict_addr[iter_num]:
            try:
                if arr_of_addr[arr_of_addr.index(word) + 1] == region_list[0]:
                    ansi = region_list[1]
                    return ansi
            except IndexError:
                if arr_of_addr[arr_of_addr.index(word) - 1] == region_list[0]:
                    ansi = region_list[1]
                    return ansi
            try:
                if not ansi:
                    for region_list in dict_addr[iter_num]:
                        if arr_of_addr[arr_of_addr.index(word) - 1] == \
                                region_list[0]:
                            ansi = region_list[1]
                            return ansi
            except IndexError:
                break


# функция обработки строки выдающая на выходе найденый регион
def kochegar(my_address):
    cur = open_db()
    # перечесление всех возможных ключевых слов
    address_levels = [
        ["область", "обл", "Область", "о"],
        ["Автономный", "авт", "автономный", "а", "округ", "окр", "ао"],
        ["город", "г", "Город", "Г", "значения"],
        ["Край", "край", "кр"],
        ["Республика", "респ", "республика", "рес"],
        ["округ", "окр"],
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
            if not ans:
                for i in range(5):
                    if not ans:
                        ans = search_by_level(i, elem, address_levels,
                                              full_adr, dict_level)
                    else:
                        break
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
