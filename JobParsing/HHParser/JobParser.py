# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os


def getPage(page, request_word):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    params = {
        'text': f'{request_word}',  # Текст фильтра. В имени должно быть слово "Аналитик"
        # 'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# Считываем первые 2000 вакансий

if __name__ == '__main__':
    with open('search_data.txt', 'r', encoding='utf-8') as file:
        for i in range(43):
            l = file.readline().strip()
            print(l)
            jsObj = json.loads(getPage(0, l))
            for page in range(0, jsObj['pages']):

                # Преобразуем текст ответа запроса в справочник Python
                if page != 0:
                    jsObj = json.loads(getPage(page, l))
                # print(jsObj['items'][0]['pages'])

                # if page == 0:
                #     with open(f'1.json', 'w', encoding='utf8') as f:
                #         f.write(json.dumps(jsObj, indent=4, ensure_ascii=False))
                #         # f.close()
                # else:
                #     with open(f'1.json', 'a', encoding='utf8') as f:
                #         f.write(json.dumps(jsObj, indent=4,  ensure_ascii=False))
                        # f.close()

                for it in jsObj['items']:
                    id = it['id']
                    req = requests.get(f'https://api.hh.ru/vacancies/{id}')  # Посылаем запрос к API
                    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
                    item = json.loads(data)
                    req.close()
                    # print(data)
                    with open('2.json', 'w', encoding='utf8') as file:
                        file.write(json.dumps(item, indent=4,  ensure_ascii=False))
                    #
                    parametrs = []
                    try:
                        print(item['published_at'],item['name'], item['salary']['from'], item['salary']['to'])
                        print(it['address']['city'], it['address']['street'], it['address']['metro'],  it['address']['raw'])
                        parametrs.append(item['specializations'][0]['profarea_name'])
                        parametrs.append(item['schedule']['name'])
                        parametrs.append(item['experience']['name'])
                        print(item['description'], item['alternate_url'], parametrs, item['address']['lat'], item['address']['lng'])
                        print()
                    except:
                        print(item['published_at'],item['name'], item['salary'], item['address'], item['description'], it['address'])
                # Проверка на последнюю страницу, если вакансий меньше 2000
                # if (jsObj['pages'] - page) <= 1:
                #     break

                # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
                time.sleep(0.25)

print('Старницы поиска собраны')