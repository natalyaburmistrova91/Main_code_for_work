# coding=utf-8
# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
from pymongo import MongoClient


LIST_OF_EMPLOYEES = []
LIST_OF_EMAILS = []
UNEXPECTED_LIST = []
WAY = r"Z:\0_Helpful information\Info for Finance\Controling lists\Unsigned AR"


def mailing_unsigned():
    ready_answer = input(f'Напоминание! Все рабочиe файлы должны лежать по следующему адресу: {WAY}\n'
                         f'Работаем с файлом current_list. Он актуальный? Y/N ').upper()
    if ready_answer == 'N':
        print("Без актуализации смысла в этом нет - обнови и возвращайся!:)")
    elif ready_answer == 'Y':
        f_5 = open(f'{WAY}\current_list.txt', 'r', encoding="utf-8") # opening list of unsigned AR
        for line in f_5:
            c = line.split()
            if c[2].isalpha() == False:
                c_key = f'{c[0]} {c[1]}'
            else:
                c_key = f'{c[0]} {c[1]} {c[2]}'
            LIST_OF_EMPLOYEES.append(c_key) # making list of employees
        f_5.close()
        sorted_set_of_employees = sorted(list(set(LIST_OF_EMPLOYEES))) # making unique and sorted list of employees

        #  Make connection to the base
        client = MongoClient('localhost', 27017)
        db = client['EmployeeInfo']
        employees = db.emloyees
        for i in sorted_set_of_employees:
            employees_info = employees.find_one({'ФИО': i})
            if employees_info is None:
                UNEXPECTED_LIST.append(i)
            else:
                LIST_OF_EMAILS.append(employees_info['Login в системе'])
        f_6 = open(f'{WAY}\list_of_emails.txt', 'w', encoding="utf-8")
        if len(UNEXPECTED_LIST) != 0:
            f_6.write(f'Вот кого я не нашел в списке 1С:\n')
            for el in UNEXPECTED_LIST:
                f_6.write(f'{el}\n')
        if len(LIST_OF_EMAILS) != 0:
            f_6.write(f'Список тех, кого нашел:\n')
            for el in LIST_OF_EMAILS:
                f_6.write(f'{el}@accenture.com\n')
        f_6.close()
        print(f'Файл с адресами выгружен в папку {WAY}')
    else:
        print("Вы ввели неверное значение")

