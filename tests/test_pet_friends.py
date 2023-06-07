import os

from api import PetFriends
from settings import valid_email, valid_password, nonvalid_password, nonvalid_email
from pic_code import p_c, p_c2


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)

def test_all_pets_with_valid_key(filter = ''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status,result = pf.list_of_pets(auth_key, filter)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result) > 0


def test_add_new_pets_with_valid_data(name='Чип', animal_type='бурундук', age='1', pet_photo1='images/P1040103.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result ['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets ['pets'])== 0:
        pet_photo = os.path.join(os.path.dirname(__file__), 'images/cat1.jpg')
        pf.ad_new_pet(auth_key, 'Васька', 'кот', '7', pet_photo)
        _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
        print('новое живтоное добавлено в тесте, список животных был пуст')
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets ['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
    my_pets = dict(my_pets)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Вика', animal_type='белка', age='4'):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_add_new_pets_without_photo(name='Гаечка', animal_type='мышка', age=3):
    ''' тест на добавление карточки животного без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.ad_new_pet_simple(auth_key, name, animal_type, age)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result ['name'] == name

def test_successful_add_photo_to_simple_pet (pet_photo1='images/Gaek.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    ''' тест на добавление фото в карточку животного без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')

    # Проверяем - если список своих питомцев не пустой, то пробуем добавить фото из файла
    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_to_self_pet(auth_key, pet_id, pet_photo)
        # Проверяем что статус ответа = 200 и фото питомца соответствует фото из файла
        assert status == 200
        assert result['pet_photo'] == p_c
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pets_with_nonvalid_age_digit(name='Чип', animal_type='бурундук', age='', pet_photo1='images/P1040103.jpg'):
    ''' тест на добавление животного с невалидными цифровыми значениями возраста'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Составляем список невалидных значений
    age1 = [-100,-10, -1, 100, 110, 2000]
    # Создаем список значений статуса в запросах
    status_list = []
    # И обращаемся к кажому невалидному значению из списка, подставляя его в запрос о добавлении питомца,
    # проверяем статус ответа, затем удаляем питомца, а значения статуса помещаем в список
    for i in range(len(age1)):
        age = str(age1[i])
        status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
        if status == 200:
            _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
            pet_id = my_pets['pets'][0]['id']
            _, _ = pf.delete_pet(auth_key, pet_id)
        if status == 200 and age1[i] == '':
            print(f'Отправка незаполненого поля успешна, FAILED TEST')
        elif status == 200 and age1[i] != '':
            print(f'Отправка {age1[i]} успешна, FAILED TEST')
        else:
            print(f'Отправка {age1[i]} не осуществлена, TEST PASSED')
        status_list.append(status)
    # Проверяем что в списке статусов ответа не встречается 200
    assert '200' not in status_list


def test_add_new_pets_with_nonvalid_age_str(name='Чип', animal_type='бурундук', age='', pet_photo1='images/P1040103.jpg'):
    ''' тест на добавление животного с невалидными строчными значениями возраста'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    age1 = ['', '  ',  '1 2', '1    2', ' 1  2 ', '''   DЙF   дLswЯ 6  860№;"?@%صسغذئآ龍門大酒<script>alert("Вы взломаны!")
    </script>秋瑞<IMG src="#">'); test' OR 1=1 # ; -- ☺☻♥♦♣♠•◘''']
    status_list = []
    for i in range(len(age1)):
        age = age1[i]
        status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
        if status == 200:
            _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
            pet_id = my_pets['pets'][0]['id']
            _, _ = pf.delete_pet(auth_key, pet_id)
        if status == 200 and age1[i] == '':
            print(f'Отправка незаполненого поля успешна, FAILED TEST')
        elif status == 200 and age1[i] != '':
            print(f'Отправка {age1[i]} успешна, FAILED TEST')
        else:
            print(f'Отправка {age1[i]} не осуществлена, TEST PASSED')
        status_list.append(status)

    assert '200' not in status_list


def test_get_api_key_for_valid_user_nonvalid_email(email= nonvalid_email, password=valid_password):
    ''' тест на получение  api ключа с неправильно введенной почтой'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result)

def test_get_api_key_for_valid_user_nonvalid_pasword(email= valid_email, password=nonvalid_password):
    ''' тест на получение  api ключа с неправильно введенным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result)

def test_get_api_key_for_nonvalid_user(email= nonvalid_email, password= nonvalid_password):
    ''' тест на получение  api ключа неавторизированаого пользователя'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result)

def test_add_new_pets_with_nonvalid_name(name='', animal_type='бурундук', age='1', pet_photo1='images/P1040103.jpg'):
    ''' тест на добавление животного с невалидными строчными значениями вида животного'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    name1 = ['', ' ', '    ', '''   DЙF   дLswЯ 6  860№;"?@%صسغذئآ龍門大酒<script>alert("Вы взломаны!")
    </script>秋瑞<IMG src="#">'); test' OR 1=1 # ; -- ☺☻♥♦♣♠•◘''', '''14jYuZsGlJjYxOYdPTJebhuJgGgWuaYBpUbxEtxKEhGtX
    iuBkyCIufWQqTAbaXlAQzaZOEvvxRgGaMKTFLduRaouihOuXjxHqPXqbjzkjPSCYbtFaqiDBnzNcJymvCsPTAEWlFBofUqdhmSpOihjBumquPfqWX
    kmEUSvsXGQAVBwZZsSXsXQYnYPrCbCGoZRoJIBOgSRJpePQWGBlPCnrIlkOdYobRLcXFgbwxRmwySAvfHLiBVyhIudSNenbvyjzZxraJzMKupefOT
    eKoNiIiAfiEKIejvoABMdFYcUWsibgfmcsDnExHGpozUFTetzoCTSdTGckvgJicwngwV7EKIoBeGuYLCouOGOSZWMSPpPFCVSagjiXZIayxvZVWkd
    omVwMjxvOxpCotcTxAsVdQSTEujFqccMxVtWQayFdFDrDOrWMsRLymSNYgVyCLuIPMlcxhzFVFhMgpRwhHYfjQVWsLpaOpkhEnkflRtqkZQgFeOeL
    m21''']
    status_list = []
    for i in range(len(name1)):
        name = name1[i]
        status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
        if status == 200:
            _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
            pet_id = my_pets['pets'][0]['id']
            _, _ = pf.delete_pet(auth_key, pet_id)
        if status == 200 and name1[i] == '':
            print (f'Отправка незаполненого поля успешна, FAILED TEST')
        elif status ==200 and name1[i] != '':
            print(f'Отправка {name1[i]} успешна, FAILED TEST')
        else:
            print(f'Отправка {name1[i]} не осуществлена, TEST PASSED')
        status_list.append(status)


    assert '200' in status_list


def test_add_new_pets_with_nonvalid_anymal_type(name='Чип', animal_type='', age='1', pet_photo1='images/P1040103.jpg'):
    ''' тест на добавление животного с невалидными строчными значениями имени'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    animal_type1 = ['', ' ', '    ', '''   DЙF   дLswЯ 6  860№;"?@%صسغذئآ龍門大酒<script>alert("Вы взломаны!")
    </script>秋瑞<IMG src="#">'); test' OR 1=1 # ; -- ☺☻♥♦♣♠•◘''', '''14jYuZsGlJjYxOYdPTJebhuJgGgWuaYBpUbxEtxKEhGtX
    iuBkyCIufWQqTAbaXlAQzaZOEvvxRgGaMKTFLduRaouihOuXjxHqPXqbjzkjPSCYbtFaqiDBnzNcJymvCsPTAEWlFBofUqdhmSpOihjBumquPfqWX
    kmEUSvsXGQAVBwZZsSXsXQYnYPrCbCGoZRoJIBOgSRJpePQWGBlPCnrIlkOdYobRLcXFgbwxRmwySAvfHLiBVyhIudSNenbvyjzZxraJzMKupefOT
    eKoNiIiAfiEKIejvoABMdFYcUWsibgfmcsDnExHGpozUFTetzoCTSdTGckvgJicwngwV7EKIoBeGuYLCouOGOSZWMSPpPFCVSagjiXZIayxvZVWkd
    omVwMjxvOxpCotcTxAsVdQSTEujFqccMxVtWQayFdFDrDOrWMsRLymSNYgVyCLuIPMlcxhzFVFhMgpRwhHYfjQVWsLpaOpkhEnkflRtqkZQgFeOeL
    m21''']
    status_list = []
    for i in range(len(animal_type1)):
        animal_type = animal_type1[i]
        status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
        if status == 200:
            _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
            pet_id = my_pets['pets'][0]['id']
            _, _ = pf.delete_pet(auth_key, pet_id)
        if status == 200 and animal_type1[i] == '':
            print(f'Отправка незаполненого поля успешна, FAILED TEST')
        elif status == 200 and animal_type1[i] != '':
            print(f'Отправка {animal_type1[i]} успешна, FAILED TEST')
        else:
            print(f'Отправка {animal_type1[i]} не осуществлена, TEST PASSED')
        status_list.append(status)

    assert '200' in status_list

def test_add_new_pets_with_big_photo(name='Чип', animal_type='бурундук', age='1', pet_photo1='images/giphy.tiff'):
    ''' тест на добавление животного с невалидным (большого объёма) форматом фото'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.ad_new_pet(auth_key, name, animal_type, age, pet_photo)
    if status == 200:
        _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
        pet_id = my_pets['pets'][0]['id']
        _, _ = pf.delete_pet(auth_key, pet_id)

    assert status != 200
    assert result['pet_photo'] != p_c2


def test_add_photo_to_simple_pet_nonvalid_type (pet_photo =''):
    ''' тест на добавление фото файлов разных расширенй в карточку животного без фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.list_of_pets(auth_key, 'my_pets')
    non_picture = ['txt.txt', 'text.doc', 'table.xls', 'presentattion.ppt', 'json.json', 'HTML_doc.html',
                       'draw.std']

    if len(my_pets['pets']) > 0:
        status_list = []
        for i in range(len(non_picture)):
            pet_photo1 = f'images/{non_picture[i]}'
            pet_photo = os.path.join(os.path.dirname(__file__), pet_photo1)
            pet_id = my_pets['pets'][0]['id']
            status, result = pf.add_photo_to_self_pet(auth_key, pet_id, pet_photo)
            if status == 200:
                print(f'Отправка {non_picture[i]} успешна, FAILED TEST')
            else:
                print(f'Отправка {non_picture[i]} не осуществлена, TEST PASSED')
        status_list.append(status)
        assert '200' not in status_list
    else:
        raise Exception("There is no my pets")


















