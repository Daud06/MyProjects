# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests
import openpyxl
import multiprocessing
# Пакет для удобной работы с данными в формате json
import json
# import multiprocess
# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os
book = openpyxl.Workbook()
sheet = book.active
cash1 = []


# with open('numbers', 'r', encoding='utf8') as f:
#     for i in range(3399):
#         s = f.readline().strip()
#         print(s)
#         cash1.append(s)



def getPage(page, request_word):

    headers = {
        # 'grant_type': 'authorization_code',
        'Authorization': 'Bearer J3F5BTVH2NMEFER955RR3QRRCHLOMJNLRDE6DEF4GDMENIAD9SQ0QNK8MFM61PPO',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }

    # Справочник для параметров GET-запроса
    params = {
        # 'grant_type': 'authorization_code'
        'text': f'{request_word}',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': [1, 2019],  # Поиск ощуществляется по вакансиям города Москва
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 100  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies/', headers = headers,  params = params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data




def write_in_excel(parametrs, str_number):
    # if str_number == 58:
    #     parametrs = ['-'] * 18

    try:
        sheet[f'A{str_number}'] = parametrs[0]
        sheet[f'B{str_number}'] = parametrs[1]
        sheet[f'C{str_number}'] = parametrs[2]
        sheet[f'D{str_number}'] = parametrs[3]
        sheet[f'E{str_number}'] = parametrs[4]
        sheet[f'F{str_number}'] = parametrs[5]
        sheet[f'H{str_number}'] = parametrs[6]
        sheet[f'I{str_number}'] = parametrs[7]
        sheet[f'J{str_number}'] = parametrs[8]
        sheet[f'K{str_number}'] = parametrs[9]
        sheet[f'L{str_number}'] = parametrs[10]
        sheet[f'M{str_number}'] = parametrs[11]
        sheet[f'N{str_number}'] = parametrs[12]
        sheet[f'O{str_number}'] = parametrs[13]
        sheet[f'P{str_number}'] = parametrs[14]
        sheet[f'Q{str_number}'] = parametrs[15]
        sheet[f'R{str_number}'] = parametrs[16]
        sheet[f'S{str_number}'] = parametrs[17]
    except:
        print(parametrs)

    if str_number % 50 == 0:
        book.save(f'HeadHunterPool2.xlsx')

# Считываем первые 2000 ваканси

def get_data(l):
    name = multiprocessing.current_process().name
    params = []
    tp = 0
    try:
        jsObj = json.loads(getPage(0, l))
    except:
        time.sleep(40)
        jsObj = json.loads(getPage(0, l))

    for page in range(0, jsObj['pages']):
        # Преобразуем текст ответа запроса в справочник Python
        if page != 0:
            try:
                jsObj = json.loads(getPage(page, l))
            except:
                time.sleep(60)
                continue

        for item in jsObj['items']:

            # if tp < 2051:
            #     tp += 1
            #     print(tp)
            #     continue
            id = item['id']
            req = requests.get(f'https://api.hh.ru/vacancies/{id}')
            data = req.text
            vacansy_info = json.loads(data)

            # with open('2.json', 'w', encoding='utf8') as fl:
            #     fl.write(json.dumps(description, indent= 4, ensure_ascii= False))
            #     fl.close()
            # break

            parametrs = []
            try:
                parametrs.append(item['contacts']['phones'][0]["country"] + item['contacts']['phones'][0]["city"] + item['contacts']['phones'][0]["number"])
                if (parametrs[-1] in cash1) or (item['contacts']['phones'][0]["city"] == '495') or (item['contacts']['phones'][0]["city"] == '800'):
                    continue
                else:
                    cash1.append(parametrs[-1])
            except:
                continue

            parametrs.append(item['id'])
            parametrs.append(item['published_at']), parametrs.append(item['name'])

            try:
                parametrs.append(item['salary']['from']), parametrs.append(item['salary']['to'])
            except:
                parametrs.append('-'), parametrs.append('-')

            try:
                parametrs.append(item['contacts']['name'])
            except:
                parametrs.append('-')

            try:
                parametrs.append(item['address']['city']),
            except:
                parametrs.append('-')
            try:
                parametrs.append(item['address']['street'])
            except:
                parametrs.append('-')
            try:
                parametrs.append(item['address']['metro']['station_name'])
            except:
                parametrs.append('-')
            try:
                parametrs.append(item['address']['raw'])
            except:
                parametrs.append('-')
            try:
                parametrs.append(
                    vacansy_info['specializations'][0]['profarea_name'] + " | " + vacansy_info['schedule'][
                        'name'] + " | " + vacansy_info['experience']['name'])
            except:
                parametrs.append('-')

            try:
                parametrs.append(vacansy_info['description'])
            except:
                parametrs.append('-')
            parametrs.append(item['alternate_url'])

            try:
                parametrs.append(item['employer']['logo_urls']['original'])
            except:
                parametrs.append('-')
            parametrs.append('Работодатель')

            try:
                parametrs.append(item['address']['lat']), parametrs.append(item['address']['lng'])
            except:
                parametrs.append('-'), parametrs.append('-')

            if name == 'SpawnPoolWorker-1':
                with open('1.json', 'a', encoding='utf8') as fr:
                    fr.write(',')
                    fr.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
                    fr.close()
            if name == 'SpawnPoolWorker-2':
                with open('4.json', 'a', encoding='utf8') as fl:
                    fl.write(',')
                    fl.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
                    fl.close()
            if name == 'SpawnPoolWorker-3':
                with open('5.json', 'a', encoding='utf8') as fr:
                    fr.write(',')
                    fr.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
                    fr.close()
            print(tp)
            # if tp == 150:
            #     tp = 0
            #     break
            # write_in_excel(parametrs, tp)
            tp+=1

            # print(k)
            # k +=1
    # print(params)
    # return tp


# def back_func(responce):
#     with open('2.json','r', encoding='utf8') as file:
#         data = json.loads(file.read())
#     # print(responce)
#
#     # for i in range(10):
#     #     for j in responce[i]:
#     #         print(j)
#     # name = responce['Pool']
#     # # parametrs = responce['list']
#     k = 2
#     for p in data:
#         try:
#             write_in_excel(p, k)
#             print(k)
#             k+=1
#         except:
#             print(k, 'error')
#             continue
#
# def first_f(x):
#     params = []
#     name = multiprocessing.current_process().name
#     if name == 'SpawnPoolWorker-1':
#         k = cash1[-1]
#     if name == 'SpawnPoolWorker-2':
#         k = cash2[-1]
#     if name == 'SpawnPoolWorker-3':
#         k = cash3[-1]
#     if name == 'SpawnPoolWorker-4':
#         k = cash4[-1]
#
#     for i in range(10):
#         for j in range(5):
#             pr = [i, j]
#             params.append(pr)
#     return params
#     # params.append(x)
#     # # print(x)
#     # return {'list': params, 'Pool': f'{name}'}



if __name__ == '__main__':

    # with multiprocessing.Pool(2) as p:
    #     with open('search_data.txt', 'r', encoding='utf8') as file:
    #         r = file.read().strip().split(',')
    #         p.map(get_data, r)
    #         p.close()
    #         p.join()
    # with open('search_data.txt', 'r', encoding='utf8') as file:
    #     k = 2
    #     for i in range(43):
    #         r = file.readline()
    #         k = get_data(r, k)
    # book.save(f'HeadHunter1.xlsx')
    with open('1.json','r', encoding='utf-8') as file:
        # r = file.read()
        # r = r.replace('\n', '').strip()
        # print(r)
        data_js1 = json.load(file)
        data1 = data_js1["main-item"]
    with open('4.json','r', encoding='utf-8') as fl:
        # r = file.read()
        # r = r.replace('\n', '').strip()
        # print(r)
        data_js2 = json.load(fl)
        data2 = data_js2["main-item"]
    # with open('5.json','r', encoding='utf-8') as file:
    #     # r = file.read()
    #     # r = r.replace('\n', '').strip()
    #     # print(r)
    #     data_js3 = json.load(file)
    #     data3 = data_js3["main-item"]
    k = 2
    # print(data)
    for p in data1:
        # print(p)
        write_in_excel(p['item'], k)
        print(k)
        k+=1
    for l in data2:
        try:
            # print(p)
            write_in_excel(l['item'], k)
            print(k)
            k+=1
        except:
            print(k, 'error')
            continue
    # for t in data3:
    #     try:
    #         # print(p)
    #         write_in_excel(t['item'], k)
    #         print(k)
    #         k+=1
    #     except:
    #         print(k, 'error')
    #         continue