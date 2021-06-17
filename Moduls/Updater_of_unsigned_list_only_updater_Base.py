# coding=utf-8
import xlrd
import xlwt
from xlutils.copy import copy
import datetime

NOW = datetime.datetime.today().date()
LIST_FROM_1C = []
MIXED_LISTS = []

WAY = r"Z:\0_Helpful information\Info for Finance\Controling lists\Unsigned AR"


def xldate_to_datetime(xldate):
    temp = datetime.datetime(1899, 12, 30)
    delta = datetime.timedelta(days=xldate)
    date = temp+delta
    return f'{date.day}.{date.month}.{date.year}'


def list_usigned_updater():

    instruction_answer = input('Вам нужна инструкция как обновить? Y/N ').upper()
    if instruction_answer == 'Y':
        ready_answer = input(f'Все рабочиe файлы должны лежать по следующему адресу: {WAY}\n'
              f'1. Открой current_list и убери всех подписавших из списка\n'
              f'2. Выгрузи список авансовых отчетов из 1С за новый месяц, который хочешь добавить.\n'
              f'3. Он должен называться ListOfAdvanceReports.xls.\n'
              f'3. Добавь в этот файл 2 столба (по номеру они будут - 2 и 3, сдвигая всю информацию на 2 вправо)\n'
              f'4. Поставь во 2 столбце 1 - если АО не подписан; 2 - если подписан, но есть комментарий '
              f'(т.е. стикер висит) и комментарий в 3 столбец\n'
              f'5. После того как закончил - запускай программу\n'
              f'6. Программа выдаст тебе файл под названием list_of_uns_month (т.е. тех, '
              f'кого ты отметил 1 или 2 во 2 столбце)\n'
              f'7. Программа спросит, замиксовать его с текущим? Если да - введи "y" или "Y", '
              f'и он объединит 2 файла - current_list и list_of_uns_month и выдаст новый - дата_new_current_list\n'
              f'8. Проверь этот файл и если все ок - кинь его в папку "RESERVED COPY OF CURRENT_LIST" \n'
              f'9. Удали старый current_list \n'
              f'10. Переименуй дата_new_current_list в current_list (в следующий раз будет обновление уже этого списка)\n'
              f'Вы готовы? Y/N ').upper()
    else:
        ready_answer = input(f'Напоминание! Все рабочиe файлы должны лежать по следующему адресу: {WAY}\n'
                             f'Вы готовы? Y/N ').upper()
    if ready_answer == 'Y':
        file_from_1c = xlrd.open_workbook(f'{WAY}\ListOfAdvanceReports.xls', formatting_info=True)
        file_from_1c_sheet = file_from_1c.sheet_by_index(0)
        for row_num in range(1, file_from_1c_sheet.nrows):
            row_line = file_from_1c_sheet.row_values(row_num)
            if row_line[1] != '':
                if row_line[1] == 1:
                    LIST_FROM_1C.append([row_line[5], row_line[3], row_line[4], row_line[2]])
                else:
                    LIST_FROM_1C.append([row_line[5], row_line[3], row_line[4], 'подписано', row_line[2]])
        LIST_FROM_1C.sort()  # sorting
        #  uploading list of unsigned AR from 1C
        f_1 = open(f'{WAY}\list_of_uns_month.txt', 'w', encoding="utf-8")
        for el in LIST_FROM_1C:
            f_1.write(f'{el[0]} {xldate_to_datetime(el[1])} {el[2]} {el[3]}\n')
        f_1.close()
        print('Список за месяц выгружен!')
        #  Asking would the user like to mix 2 lists (old and the new one)
        mix_lists = input('Вы хотите объединить текущий список со списком за месяц? Y/N ').upper()
        if mix_lists == 'Y':
            f_2 = open(f'{WAY}\list_of_uns_month.txt', 'r', encoding="utf-8")
            for line in f_2:
                MIXED_LISTS.append(line)
            f_2.close()
            f_3 = open(f'{WAY}\current_list.txt', 'r', encoding="utf-8")
            for line in f_3:
                MIXED_LISTS.append(line)
            f_3.close()
            MIXED_LISTS.sort()
            f_4 = open(f'{WAY}\{NOW}_new_current_list.txt', 'w', encoding="utf-8")
            for el in MIXED_LISTS:
                f_4.write(f'{el}')
            f_4.close()
            print(f'Новый список выгружен по адресу {WAY}! ')
    else:
        print('Ну что ж, в другой раз!')

