import csv


users_list = [
        {'name': 'Маша', 'age': 25, 'job': 'Scientist'},
        {'name': 'Вася', 'age': 8, 'job': 'Programmer'},
        {'name': 'Эдуард', 'age': 48, 'job': 'Big boss'},
        ]
with open('users.csv', 'w', encoding='utf-8') as users:
    fields = ['name', 'age', 'job']
    writer = csv.DictWriter(users, fields, delimiter=';')
    writer.writeheader()
    for user in users_list:
        writer.writerow(user)


