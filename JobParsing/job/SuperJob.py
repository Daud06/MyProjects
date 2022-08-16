# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests
import openpyxl
# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

book = openpyxl.Workbook()
sheet = book.active




def getPage(page, request_word):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    params = {
        # 'Authorization' : 'Bearer v3.r.136893216.24e17462a3337d522e3ab8dae57a85a2729519b2.3a5fa8ef2c45e107ebcbf68c52c05a9c5a398cab',
        'app_key': 'v3.r.136893216.6fbd67d248a53d816721b9f6b784e724240941c8.a62ec4d030650958b002ac95d24602c3aa87505f',
        # 'client_secret'
        # 'app_key': '1995',
        'keyword': f'{request_word}',  # Текст фильтра. В имени должно быть слово ""
        # 'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'count': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.superjob.ru/2.0/vacancies/', params)  # Посылаем запрос к API
    data = req.text # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# Считываем первые 2000 вакансий

if __name__ == '__main__':
    with open('search_data.txt', 'r', encoding='utf-8') as file:
        for i in range(43):
            l = file.readline().strip()
            print(l)
            jsObj = json.loads(getPage(0, l))
            # print(jsObj)
            k = 2
            with open(f'1.json', 'w', encoding='utf8') as f:
                f.write(json.dumps(jsObj, indent=4, ensure_ascii=False))



print('Старницы поиска собраны')