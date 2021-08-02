from pymongo import MongoClient



client = MongoClient('localhost', 27017)
db = client['EmployeeInfo']
employees = db.emloyees


tab_number = int(input('Введите табельный номер сотрудника: '))
employee = employees.find_one({'Табельный номер': tab_number})
print(employee)
employees.delete_one({'Табельный номер': tab_number})
print('Удалил')

#
#     print('Проверим есть ли записи после очистки. Они выведутся если есть. ')
#     for employee in employees.find({}):
#         print(employee)
#     print('База очищена.')



if __name__ == '__mane__':
    total_delete()
    # check base
    client = MongoClient('localhost', 27017)
    db = client['EmployeeInfo']
    employees = db.emloyees

    for employee in employees.find({}):
        print(employee)