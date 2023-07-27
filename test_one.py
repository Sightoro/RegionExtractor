import random
import sqlite3

from main import kochegar
from mimesis import Address


def test_full_with_index():
    levels = ["область", "обл", "Область", "о",
              "Автономный", "авт", "автономный", "а", "округ", "окр",
              "ао",
              "Край", "край", "кр",
              "Республика", "респ", "республика", "рес", "регион",
              "Регион",
              "рег", "р",
              "округ", "окр"]
    address = Address('ru')
    n = random.randrange(5, 10)
    all_addresses1 = []
    ans = []
    con = sqlite3.connect("addresses_database.db")
    cur = con.cursor()
    for i in range(n):
        index = address.postal_code()
        reg = address.region()
        cur.execute(
            "SELECT region FROM {table} WHERE `index` = \
            {index}".format(table="address", index=str(
                "'" + str(index)[0:6] + "'")))
        ansi = cur.fetchall()
        if ansi:
            tmp = ansi[0][0]
            tm = []
            print(tmp.split(" "))
            for i in tmp.split(" "):
                if i:
                    tm.append(i)
            ans.append(" ".join(tm).lower())
        else:
            if reg.split()[len(reg.split()) - 1] in levels:
                ans.append(reg.lower())
        addr = "{index} {region} {city} {street}".format(
            index=index, region=reg,
            city=address.city(), street=address.address()
        )
        all_addresses1.append(addr.split())
    cur.close()
    ans1 = kochegar(all_addresses1)
    assert sorted(ans1) == sorted(ans)
