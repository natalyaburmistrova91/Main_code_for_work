# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
from Updater_of_unsigned_list_only_mailing_Base import mailing_unsigned
from Updater_of_unsigned_list_only_updater_Base import list_usigned_updater


def unsigned_list_updater_and_mailing():
    working_step = int(input('Что вы хотите сделать? 1. Если хотите обновить список 2. Если хотите отправить рассылку: '))
    if working_step == 1:
        list_usigned_updater()
    elif working_step == 2:
        mailing_unsigned()
    else:
        print('Вы ввели неверное значение! ')