import sys
sys.path.append(r"Z:\0_Helpful information\Info for Finance\Python_Moduls\Moduls")
from Payment_creator_Base import payment_creator_base
from Base import base
from Blank_of_report_filler import blank_of_report_filler
from PIT_filler_Base import pit_filler
from Updater_of_unsigned_list_and_mailing_Base import unsigned_list_updater_and_mailing


while True:
        answer = input('Что вы хотите сделать? \n1. Поработать с базой данных \n2. Создать платежные поручения '
                       '\n3. Заполнить бланк на загран командировку \n4. Сформировать файл PIT \n5. Обновить список '
                       'неподписанных АО и отправить рассылку\n6. Выйти из программы \nВаш выбор: ')
        if answer == '1':
            base()
        elif answer == '2':
            payment_creator_base()
        elif answer == '3':
            blank_of_report_filler()
        elif answer == '4':
            pit_filler()
        elif answer == '5':
            unsigned_list_updater_and_mailing()
        else:
            print('Хорошего дня!')
            break