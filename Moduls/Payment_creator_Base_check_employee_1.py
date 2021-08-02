import datetime
from pymongo import MongoClient
import xlrd


def check_employee_1():

    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    employee_none = []
    employee_req = []
    employee_avail = []

    handle_payment = input("Будут платежи не из выгруженного списка 1С? Y/N ").upper()

    while handle_payment == 'Y':
        tab_number = int(input('Введите табельный номер сотрудника (чтобы закончить, введите 0): '))
        if tab_number == 0:
            f_1 = open("C:\python_working_files\list of tab numbers (handle payment).txt", 'w', encoding="utf-8")
            for r in employee_req:
                f_1.write(" ".join([str(r), '\n']))
            for n in employee_none:
                f_1.write(" ".join([str(n), '\n']))
            for a in employee_avail:
                f_1.write(" ".join([str(a), '\n']))
            f_1.close()
            break
        employee_info = employees.find_one({'Табельный номер': tab_number})
        if employee_info == None:
            print(f'!ВНИМАНИЕ! Статус 3. Сотрудника с {tab_number} нет в базе!')
            employee_none.append(tab_number)
        else:
            if employee_info["Реквизиты"] == 'None' \
                    or employee_info["Банк"] == 'None' \
                    or employee_info["Статус"] == 'None':
                message_text = f'!ВНИМАНИЕ! Статус 2. {employee_info["ФИО"]} есть в базе. Реквизитов не хватает. '
                if employee_info.get('Комментарий') is not None:
                    message_text += f'КОММЕНТАРИЙ: {employee_info["Комментарий"]}'
                print(message_text)
                employee_req.append(tab_number)
            else:
                message_text = f'Статус 1. {employee_info["ФИО"]}. Все ок! '
                if employee_info['Статус'].lower() == 'нерезидент':
                    message_text += f'ВНИМАНИЕ! Сотрудник НЕРЕЗИДЕНТ!'
                print(message_text)
                employee_avail.append(tab_number)

    one_c_payment = input("Будут платежи из выгруженного файла 1С? Y/N ").upper()
    if one_c_payment == 'Y':
        one_c_payment_file = xlrd.open_workbook('C:\python_working_files\list_of_AR.xls', formatting_info=True)
        one_c_payment_sheet = one_c_payment_file.sheet_by_index(0)
        for row_num in range(1, one_c_payment_sheet.nrows):
            row_line = one_c_payment_sheet.row_values(row_num)
            employee_name = row_line[3].split()
            employee_name_real = ' '.join(employee_name)
            employee_info = employees.find_one({'ФИО': employee_name_real})
            if employee_info is None:
                print(f'!ВНИМАНИЕ! Статус 3. Сотрудника {employee_name_real} нет в базе!')
            else:
                if employee_info["Реквизиты"] == 'None' \
                        or employee_info["Банк"] == 'None' \
                        or employee_info["Статус"] == 'None':
                    message_text = f'!ВНИМАНИЕ! Статус 2.{employee_name_real} есть в базе. Реквизитов не хватает. '
                    if employee_info.get('Комментарий') is not None:
                        message_text += f'КОММЕНТАРИЙ: {employee_info["Комментарий"]}'
                    print(message_text)
                else:
                    message_text = f'Статус 1. {employee_name_real}. Все ок! '
                    if employee_info['Статус'].lower() == 'нерезидент':
                        message_text += f'ВНИМАНИЕ! Сотрудник НЕРЕЗИДЕНТ!'
                    print(message_text)

