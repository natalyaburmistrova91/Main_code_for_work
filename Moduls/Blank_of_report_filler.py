# Библиотеки
import xlrd
import xlwt
from xlutils.copy import copy
from pymongo import MongoClient
from Blank_of_report_filler_Parsing_CB import payment_parsing_CB

TERMINS_DICTIONARY = {
    1: 'HOTEL',
    2: 'AEROEXPRESS',
    3: 'TRAIN TICKET',
    4: 'AIR TICKET'
}
CURRENCY_NAME_DICTIONARY = {
    '1': 'USD',
    '2': 'EUR',
    '3': 'GBP',
    '4': 'RUB',
}

CURRENCY_RATE_DICTIONARY = {
}

LIST_OF_TAX_VALUES = ['Resident (13%)', 'Resident (15%)', 'NON-Resident']
LIST_OF_TAX_RATES = [0.87, 0.85, 0.7]


def round_number1000(number1000):
    end = int(number1000) % 10
    if end >= 5:
        result = int(number1000/10) + 1
    else:
        result = int(number1000/10)
    return result


def set_style(set_bottom, set_left=xlwt.Borders.NO_LINE, set_right=xlwt.Borders.NO_LINE, set_top=xlwt.Borders.NO_LINE, num_format_str=None):
    font = xlwt.Font()  # устанавливаем курсив
    font.name = 'Book Antiqua'
    font.height = 220
    align = xlwt.Alignment()
    align.horz = xlwt.Alignment.HORZ_CENTER
    border = xlwt.Borders()
    border.bottom = set_bottom
    border.left = set_left
    border.right = set_right
    border.top = set_top
    style = xlwt.XFStyle()
    style.font = font
    style.alignment = align
    style.borders = border
    if num_format_str is not None:
        style.num_format_str = num_format_str
    return style


def try_number(inputting_value):
    try:
        result = float(inputting_value)
    except ValueError:
        b = inputting_value.split(',')
        result = float('.'.join(b))
    return result


def blank_of_report_filler():

    client = MongoClient('localhost', 27017)
    db = client['CountryRatesInfo']
    country_rates = db.country_rates


    def foreign_perdiem_accumulating(position, country, md):
        total_foreign = foreign_perdiem_counting(position, country, md)
        total_for_in_rub_keep = total_foreign[0]
        number_of_days_country = total_foreign[1]
        daily_rate_net_keep = total_for_in_rub_keep / number_of_days_country
        if daily_rate_net_keep > 2500 * 1000:
            non_taxable_amount_keep = 2500 * number_of_days_country * 1000
        else:
            non_taxable_amount_keep = total_for_in_rub_keep
        return [total_for_in_rub_keep, non_taxable_amount_keep]


    def foreign_perdiem_counting(position, country, md):
        #  считаем зарубежные суточные в 1 стране:
        country_check = country_rates.find_one({'Страна': country, 'MD': md})
        if country_check is None:
            currency_name = input('Введите название валюты в стране (1. USD / 2. EUR / 3. GBP): ')
        else:
            currency_name = country_check['Валюта']
        new_employee.get_sheet(0).write(position, 0, currency_name,
                                        style2)  # записываем название валюты в файл из словаря
        currency_rate_keep = CURRENCY_RATE_DICTIONARY.get(currency_name)
        currency_rate_print = currency_rate_keep / 10000
        new_employee.get_sheet(0).write(position, 3, currency_rate_print, style2)  # записываем курс в файл
        if country_check is None:
            rate_in_country = int(input('Введите ставку в стране: '))
        else:
            country_rate = int(input(
                'Какая ставка (введите цифру)? (1. Отельная / 2. Отельная с планом '
                '/ 3. Долгосрочная аренда (Unserviced Accommodation)  '
                '/ 4. Краткосрочная аренда (Serviced Accommodation): '))
            if country_rate == 1:
                rate_in_country = country_check['Отельная ставка']
            elif country_rate == 2:
                rate_in_country = country_check['Отельная ставка с планом']
            elif country_rate == 3:
                rate_in_country = country_check['Долгосрочная аренда (Unserviced Accommodation)']
            else:
                rate_in_country = country_check['Краткосрочная аренда (Serviced Accommodation)']
        new_employee.get_sheet(0).write(position, 1, rate_in_country, style2)  # записываем ставку в файл
        daily_rate_net_keep = round_number1000((rate_in_country * currency_rate_keep) / 10) * 10  # храним в 1000 больше
        daily_rate_net_print = daily_rate_net_keep / 1000  # выводим с запятой
        new_employee.get_sheet(0).write(position, 5, daily_rate_net_print, style4)  # записываем дневную ставку в файл
        number_of_days_country = int(input('Введите количество зарубежных дней: '))
        new_employee.get_sheet(0).write(position, 6, number_of_days_country,
                                        style2)  # записываем количество дней в файл
        total_for_in_rub_keep = int(daily_rate_net_keep * number_of_days_country)  # храним в 1000 больше
        total_for_in_rub_print = total_for_in_rub_keep / 1000  # выводим с запятой
        new_employee.get_sheet(0).write(position, 7, total_for_in_rub_print, style4)  # записываем итого в рублях NET
        return [total_for_in_rub_keep, number_of_days_country]


    def other_expense_adder(position):
        type_of_expense_answer = int(
            input('Какой тип расхода? ( 1. Hotel / 2. Aeroexpress / 3. Train ticket / 4. Air ticket ) '))
        type_of_expense = TERMINS_DICTIONARY.get(type_of_expense_answer)
        new_employee.get_sheet(0).write(position, 1, type_of_expense, style4)  # Other expenses TOTAL in total sheet
        currency_of_expense = input('В какой валюте? (1. USD / 2. EURO / 3. GBP / 4. RUB) ')
        currency_check = CURRENCY_NAME_DICTIONARY.get(currency_of_expense)
        if currency_check is not None:
            currency_of_expense = currency_check
        new_employee.get_sheet(0).write(position, 4, currency_of_expense, style4)  # Currency
        if CURRENCY_RATE_DICTIONARY.get(currency_of_expense) is None:
            currency_rate_print = try_number(input('Введите курс: '))
            currency_rate_keep = int(currency_rate_print * 10000)  # храним в 10 000 больше
            CURRENCY_RATE_DICTIONARY[currency_of_expense] = currency_rate_keep
        currency_rate_keep = CURRENCY_RATE_DICTIONARY.get(currency_of_expense)
        currency_rate_print = currency_rate_keep / 10000
        new_employee.get_sheet(0).write(position, 5, currency_rate_print, style2)  # rate
        amount_of_exp_other_print = try_number(input("Введите сумму расхода: "))
        amount_of_exp_other_keep = amount_of_exp_other_print
        new_employee.get_sheet(0).write(position, 6, amount_of_exp_other_print, style4)  # Amount in currency
        amount_of_exp_RUB_keep = round_number1000((amount_of_exp_other_keep * currency_rate_keep) / 10) * 10
        amount_of_exp_RUB_print = amount_of_exp_RUB_keep / 1000
        new_employee.get_sheet(0).write(position, 7, amount_of_exp_RUB_print, style4)  # Amount in RUB
        return amount_of_exp_RUB_keep

    # Base Country rate connection
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    #  Opening template
    blank_of_report = xlrd.open_workbook(r'Z:\0_Helpful information\Info for Finance\Python_Moduls\Templates\blank_of_report.xls', formatting_info=True)
    #  Coping file for fulfilling
    new_employee = copy(blank_of_report)
    #  Set styles
    style1 = set_style(xlwt.Borders.THIN)
    style2 = set_style(xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN)
    style3 = set_style(xlwt.Borders.MEDIUM, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN)
    style4 = set_style(xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, '#,##0.00')
    style5 = set_style(xlwt.Borders.MEDIUM, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, '#,##0.00')
    # спрашиваем пользователя табельный номер сотрудника
    tab_number = int(input('Введите табельный номер сотрудника: '))
    employee_info = employees.find_one({'Табельный номер': tab_number})
    if employee_info is None:
        print("Сотрудника нет в базе!")
    else:
        print(f"Работаем с сотрудником {employee_info['ФИО']}!")
        # спрашиваем пользователя какой датой оформлять АО:
        course_filler_status = input('Дата оформления АО: 1. текущий день 2. завтрашний день 3. Введите свою дату в формате: ДД/ММ/ГГГГ ')
        if course_filler_status == '1':
            date_of_AR, CURRENCY_RATE_DICTIONARY = payment_parsing_CB(1)
        elif course_filler_status == '2':
            date_of_AR, CURRENCY_RATE_DICTIONARY = payment_parsing_CB(2)
        else:
            date_of_AR, CURRENCY_RATE_DICTIONARY = payment_parsing_CB(course_filler_status)
        new_employee.get_sheet(0).write(1, 4, date_of_AR, style1)  # дата авансового отчета
        # оформляем документ
        order_date = input('Введите дату приказа: ')
        new_employee.get_sheet(0).write(0, 4, order_date, style1)  # дата приказа
        country = (input('Введите страну (-ы) командирования: ')).upper()
        new_employee.get_sheet(0).write(1, 7, country, style1)  # страна назначения
        date_of_begin = input('Введите дату начала командировки (в формате  DD MONTH): ')
        new_employee.get_sheet(0).write(3, 7, date_of_begin, style1)  # дата начала нахождения в командировке
        date_of_end = input('Введите дату окончания командировки (в формате  DD MONTH): ')
        new_employee.get_sheet(0).write(3, 9, date_of_end, style1)  # дата окончания нахождения в командировке
        name_of_employee = employee_info['Login в системе'].upper()
        new_employee.get_sheet(0).write(7, 2, name_of_employee, style1)  # имя сотрудника
        # объявляем аккумулятивные переменные
        non_taxable_amount_keep = 0
        total_amount_net_keep = 0
        # считаем зарубежные суточные
        position = 28
        country1 = foreign_perdiem_accumulating(position, country, employee_info['MD'])
        non_taxable_amount_keep += country1[1]
        total_amount_net_keep += country1[0]
        # Уточняем будут ли другого типа зарубежные суточные
        another_foreign_perdiem = input('Будут другого типа зарубежные суточные? (апарты или другая страна) Y/N ').upper()
        if another_foreign_perdiem == 'Y':
            position += 1
            country2 = foreign_perdiem_accumulating(position, country, employee_info['MD'])
            non_taxable_amount_keep += country2[1]
            total_amount_net_keep += country2[0]

        #  считаем локальные суточные:
        rate_local = input('Локальная ставка отельная? Y/N ').upper()
        if rate_local == 'Y':
            rate_in_local = 2092
        else:
            rate_in_local = 1609
        new_employee.get_sheet(0).write(31, 5, rate_in_local, style4)  # записываем в файл тип локальной ставки

        number_of_days_local = int(input('Введите количество локальных дней: '))
        new_employee.get_sheet(0).write(31, 6, number_of_days_local, style3)  # записываем в файл количество дней локальных

        total_loc = rate_in_local * number_of_days_local
        new_employee.get_sheet(0).write(31, 7, total_loc, style5)  # записываем в рублях NET локальная

        #  считаем тотал по суточным NET:
        total_amount_net_keep += total_loc * 1000
        total_amount_net_print = total_amount_net_keep / 1000
        new_employee.get_sheet(0).write(32, 7, total_amount_net_print, style5)  # записываем в файл итого в рублях

        #  defining tax status of the employee
        list_of_tax_values_local = list(enumerate(LIST_OF_TAX_VALUES))

        while True:
            try:
                resident_status = int(input(f'Считаем Gross. Выберите налоговый статус сотрудника:'
                                            f' {list_of_tax_values_local}'))
            except ValueError:
                print('Вы ввели неверное значение. Попробуйте еще раз, пожалуйста.')
            if resident_status in range(len(LIST_OF_TAX_VALUES)):
                resident_status_print = LIST_OF_TAX_VALUES[resident_status]
                rate = LIST_OF_TAX_RATES[resident_status]
                break
            else:
                print('Вы ввели неверное значение. Попробуйте еще раз, пожалуйста.')

        new_employee.get_sheet(0).write(33, 1, resident_status_print, style3)  #  записываем в файл статус сотрудника

        # доначисляем локальную сумму non-taxable к основной
        non_taxable_amount_keep += 700 * number_of_days_local * 1000
        non_taxable_amount_print = non_taxable_amount_keep / 1000
        new_employee.get_sheet(0).write(34, 7, non_taxable_amount_print, style4) #  записываем в файл non tax amount per diem

        # определяем сумму taxable NET
        taxable_amount_net_keep = total_amount_net_keep - non_taxable_amount_keep
        taxable_amount_net_print = taxable_amount_net_keep / 1000
        new_employee.get_sheet(0).write(35, 7, taxable_amount_net_print, style4)  # записываем в файл Taxable amount NET

        # определяем сумму taxable GROSS
        taxable_amount_gross_keep = round_number1000(taxable_amount_net_keep / rate) * 10
        taxable_amount_gross_print = taxable_amount_gross_keep / 1000
        new_employee.get_sheet(0).write(36, 7, taxable_amount_gross_print, style5)  # записываем в файл Taxable amount GROSS

        # определяем сумму TOTAL GROSS
        total_per_diem_keep = taxable_amount_gross_keep + non_taxable_amount_keep
        total_per_diem_print = total_per_diem_keep / 1000
        new_employee.get_sheet(0).write(37, 7, total_per_diem_print, style5)  # записываем в файл TOTAL GROSS

        # определяем сумму PIT
        pit = ((taxable_amount_gross_keep - taxable_amount_net_keep) / 1000)
        new_employee.get_sheet(0).write(38, 7, pit, style5)  # записываем в файл PIT

        total_expenses_keep = total_per_diem_keep
        total_expenses_print = total_per_diem_print

        # Заполняем таблицу по расходам
        new_employee.get_sheet(0).write(10, 5, total_per_diem_print, style4)  # записываем в файл в таблицу общие суточные GROSS

        # определяем будут ли другие расходы
        other_expenses = input('Будут другие расходы? Y/N ').upper()
        position = 10
        while other_expenses == 'Y': #  Заполняем прочие расходы
            position += 1
            other_expense_keep = other_expense_adder(position)
            total_expenses_keep += other_expense_keep
            other_expenses = input('Будут другие расходы? Y/N ').upper()
        total_expenses_print = total_expenses_keep / 1000
        new_employee.get_sheet(0).write(23, 4, total_expenses_print, style4)  #  записываем в файл тотал по расходам

        # определяем был ли аванс
        try:
            advance_print = float(input("Был аванс? Если да - введите сумму, если нет - 0: "))
        except ValueError:
            advance_print = 0
        advance_keep = advance_print * 1000
        new_employee.get_sheet(0).write(24, 4, advance_print, style4)  #  записываем в файл аванс
        # определяем баланс сотрудника (к выплате или удержанию)
        balance_keep = total_expenses_keep - advance_keep
        balance_print = balance_keep / 1000
        new_employee.get_sheet(0).write(25, 4, balance_print, style5)  #  записываем в файл баланс (удержание или доплата)

        new_employee.save(f'Z:/0_Helpful information/Info for Finance/PIT/Иностранные формы/{employee_info["ФИО"]} {date_of_begin}-{date_of_end}.xls')

        print(r'Бланк выгружен по адресу Z:\0_Helpful information\Info for Finance\PIT\Иностранные формы')
