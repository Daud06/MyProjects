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

# bil = [900,902,903,904,905,906,908,909,950,951,953,960,961,962,963,964,965,966,967,968,969,980,983,986]
# mts = [901,902,904,908,910,911,912,913,914,915,916,917,918,919,950,978,980,981,982,983,984,985,987,988,989]
# meg = [902,904,908,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,936,937,938,939,950,951,999]
# tele2 = [900,901,902,904,908,950,951,952,953,958,977,991,992,993,994,995,996,999]

cash1 = []
params = []

def getPage(page, request_word):
    """
    Создаем метод для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """

    # Справочник для параметров GET-запроса
    headers = {
        'Authorization': 'Bearer v3.r.136893216.5ced529193c600677daff4ee5101371d9555e542.d2637f273a2d5de6b5f13d96bb9ffbdaa67089fb'
    }

    params = {
        'app_key': 'v3.r.136893216.6fbd67d248a53d816721b9f6b784e724240941c8.a62ec4d030650958b002ac95d24602c3aa87505f',
        'keyword': f'{request_word}',  # Текст фильтра. В имени должно быть слово ""
        'page': page,  # Индекс страницы поиска на HH
        'count': 100, # Кол-во вакансий на 1 странице
        'period': 0,
        'town' : 'Москва'
    }

    req = requests.get('https://api.superjob.ru/2.0/vacancies/', headers = headers, params = params)  # Посылаем запрос к API
    time.sleep(0.5)
    data = req.text # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data




def write_in_excel(parametrs, str_number):
    # operator = '-'
    # try:
    #     meg.index(int(parametrs[0][1:4:]))
    #     operator = 'МЕГАФОН'
    # except:
    #     try:
    #         bil.index(int(parametrs[0][1:4:]))
    #         operator = 'БИЛ'
    #     except:
    #         try:
    #             tele2.index(int(parametrs[0][1:4:]))
    #
    #    operator = 'ТЕЛЕ2'
    #         except:
    #             pass

    sheet[f'A{str_number}'] = parametrs[0]
    sheet[f'B{str_number}'] = parametrs[1]
    sheet[f'C{str_number}'] = parametrs[2]
    sheet[f'D{str_number}'] = parametrs[3]
    sheet[f'E{str_number}'] = parametrs[4]
    sheet[f'F{str_number}'] = parametrs[5]
    # sheet[f'G{str_number}'] = operator
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
    if str_number % 50 == 0:
        book.save('SuperJob2.xlsx')

# Считываем первые 2000 ваканси

def get_data(l, tp):
    name = multiprocessing.current_process().name
    # params = []
    try:
        jsObj = json.loads(getPage(0, l))
    except:
        time.sleep(40)
        jsObj = json.loads(getPage(0, l))

    # with open('3.json', 'w', encoding='utf8') as f:
    #     f.write(json.dumps(jsObj,indent=4, ensure_ascii=False))
    #     f.close()

    count = (jsObj['total'] // 100) + 1

    for page in range(0, count):

        # Преобразуем текст ответа запроса в справочник Python
        if page != 0:
            try:
                jsObj = json.loads(getPage(page, l))
            except:
                time.sleep(60)
                continue

        for it in jsObj['objects']:

            parametrs = []
            try:
                parametrs.append(it['phone'])
                if (parametrs[-1] in cash1) or (parametrs[-1][4:7:] == '495') or (parametrs[-1][4:7:] == '800'):
                    continue
                else:
                    cash1.append(it['phone'])
            except:
                continue
            try:

                parametrs.append(time.strftime("%D %H:%M", time.localtime(it['date_published']))), parametrs.append(it['id'])
                parametrs.append(it['profession']), parametrs.append(str(it['payment_from']) + '-' + str(it['payment_to'])),
                parametrs.append(it['contact']), parametrs.append(it['town']['title']), parametrs.append(str(it['metro']))
                parametrs.append(it['address'])
                # if ('Московская область' not in parametrs[-1]) and ('Москва' not in parametrs[-1]):
                #     continue
                try:
                    dscr = it['vacancyRichText'].strip().replace("\n", "")
                except:
                    dscr = '-'
                parametrs.append(dscr), parametrs.append(it['link']),
                parametrs.append(it['client_logo'])
                parametrs.append('занятость: ' + it['type_of_work']['title'] + ' | ' + 'место работы: ' + it['place_of_work']['title'] + ' | ' + 'Опыт: ' + it['experience']['title'])
                parametrs.append(it['agency']['title']), parametrs.append(it['latitude']), parametrs.append(it['longitude'])
            except:
                continue

            # if name == 'SpawnPoolWorker-1':
            #     with open('1.json', 'a', encoding='utf8') as fr:
            #         fr.write(',')
            #         fr.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            #         fr.close()
            # if name == 'SpawnPoolWorker-2':
            #     with open('4.json', 'a', encoding='utf8') as fl:
            #         fl.write(',')
            #         fl.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            #         fl.close()
            # if name == 'SpawnPoolWorker-3':
            #     with open('5.json', 'a', encoding='utf8') as fp:
            #         fp.write(',')
            #         fp.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            #         fp.close()
            # params.append(parametrs)
            print(tp)
            write_in_excel(parametrs, tp)
            # if tp == 100:
            #     tp = 0
            #     break
            tp+=1
    return tp







if __name__ == '__main__':

    # with multiprocessing.Pool(3) as p:
    #     with open('search_data.txt', 'r', encoding='utf8') as file:
    #         r = file.read().strip().split(',')
    #         print(r)
    #         p.map(get_data, r)
    #         p.close()
    #         p.join()
    with open('search_data.txt', 'r', encoding='utf8') as file:
        k = 2
        for i in range(43):
            r = file.readline()
            k = get_data(r, k)

    # with open('1.json','r', encoding='utf-8') as file:
    #     # r = file.read()
    #     # r = r.replace('\n', '').strip()
    #     # print(r)
    #     data_js1 = json.load(file)
    #     data1 = data_js1["main-item"]
    # with open('4.json','r', encoding='utf-8') as file:
    #     # r = file.read()
    #     # r = r.replace('\n', '').strip()
    #     # print(r)
    #     data_js2 = json.load(file)
    #     data2 = data_js2["main-item"]
    # with open('5.json','r', encoding='utf-8') as file:
    #     # r = file.read()
    #     # r = r.replace('\n', '').strip()
    #     # print(r)
    #     data_js3 = json.load(file)
    #     data3 = data_js3["main-item"]
    # k = 2
    # # print(data)
    # for p in data1:
    #     # print(p)
    #     write_in_excel(p['item'], k)
    #     print(k)
    #     k+=1
    # for p in data2:
    #     try:
    #         # print(p)
    #         write_in_excel(p['item'], k)
    #         print(k)
    #         k+=1
    #     except:
    #         print(k, 'error')
    #         continue
    # for p in data3:
    #     try:
    #         # print(p)
    #         write_in_excel(p['item'], k)
    #         print(k)
    #         k+=1
    #     except:
    #         print(k, 'error')
    #         continue





