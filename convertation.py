import os
import pathlib


os.system("mv *.dbf address.dbf")
try:
    os.system("dbf-to-sqlite address.dbf addresses_database.db")
    # определение пути
    currentDirectory = pathlib.Path('.')
    # определение шаблона
    currentPattern = "addresses_database.db"
    flag = []
    for currentFile in currentDirectory.glob(currentPattern):
        flag.append(currentFile)
    if flag:
        print("DB is created")
    else:
        print("DB didn't create in directory")
except SystemError:
    print("System Error, try again.")
