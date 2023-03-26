import requests


def get_str(text):
    my_str = ''
    for element in text:
        if element not in ['{', '}', '"', '/']:
            index = text.find(element)
            if index > 0:
                if text[index - 1] == '/' and text[index] == 'n':
                    continue
            my_str += element
    return my_str


def print_adv(my_str):
    my_list = my_str.split(",")
    for element in my_list:
        print('   ', element)


print('Post-запрос:')
data = requests.post('http://127.0.0.1:5000/adv/',
                     json={
                         'header': 'Lada Samara 2108',
                         'description': 'From pensioner garage. Not used at all',
                         'owner': 'O.Bender',
                     },)
print('Статус: ', data.status_code)
my_str = get_str(data.text)
print('Добавлено объявление:')
print_adv(my_str)

dictionary2 = dict(subString.split(":") for subString in my_str.split(","))
new_adv_id = dictionary2['id']

print('Get-запрос:')
data = requests.get(f'http://127.0.0.1:5000/adv/{int(new_adv_id)}/',)
print('Статус: ', data.status_code)
my_str = get_str(data.text)
my_list = my_str.split(",")
print('Получено объявление:')
print_adv(my_str)

print('Patch-запрос:')
data = requests.patch(f'http://127.0.0.1:5000/adv/{int(new_adv_id)}/',
                     json={
                         'header': 'BELAZ-75710',
                         'description': 'Absolutly new track',
                         'owner': 'A.Lucashenko'
                     },)
print('Статус: ', data.status_code)
my_str = get_str(data.text)
my_list = my_str.split(",")
print('Исправлено объявление:')
print_adv(my_str)

print('Delete-запрос:')
print('Статус: ', data.status_code)
data = requests.delete(f'http://127.0.0.1:5000/adv/{int(new_adv_id)}/',)
print('Удалено объявление с id: ', new_adv_id)







# dictionary2 = dict(subString.split(":") for subString in my_str.split(","))
#
# print(f'Advertisment with id={new_adv_id} {dictionary2["status"]}')