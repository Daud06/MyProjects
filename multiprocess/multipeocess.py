from selenium import webdriver
from time import sleep
import multiprocessing
import datetime
import openpyxl
import random
import json
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By as by

book = openpyxl.load_workbook('Avito2.xlsx')
sheet = book.active
# k = 492 i = 1220
ua = ['Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
      'Mozilla/5.0 (iPhone; CPU iPhone OS 12_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/103.0 Mobile/15E148 Safari/605.1.15',
      'Mozilla/5.0 (Windows Mobile 10; Android 10.0; Microsoft; Lumia 950XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36 Edge/40.15254.603',
      'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 YaBrowser/22.7.4.658 Mobile/15E148 Safari/604.1',
      'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36',
      'Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Mobile Safari/537.36'
      ]


WIDTH = 400
HEIGHT = 600
PIXEL_RATIO = 3.0
# UA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36'
mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": random.choice(ua) }
options = webdriver.ChromeOptions()
options.add_experimental_option('mobileEmulation', mobileEmulation)


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}
cash = []
with open('phone_numbers', 'r', encoding='utf8') as up:
    l = up.read().strip()
    # l = l.replace('+','')
    l = l.replace('\xa0', ' ')
    cash = l.split('\n')
    # print(cash)


# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path='C:/Users/Дауд/PycharmProjects/untitled/chromedriver', options = options)
# driver.get('https://www.google.com/')


# with open('link_url_avito', 'r', encoding='utf8') as fr:
#     for i in range(1658):
#         cash.append(fr.readline())



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
        sheet[f'G{str_number}'] = parametrs[6]
        sheet[f'H{str_number}'] = parametrs[7]
        sheet[f'I{str_number}'] = parametrs[8]
        sheet[f'J{str_number}'] = parametrs[9]
        sheet[f'K{str_number}'] = parametrs[10]
        sheet[f'L{str_number}'] = parametrs[11]
    except:
        print(parametrs)
    if str_number % 10 == 0:
        book.save('Avito2.xlsx')

def get_data(l):
    # k = 2
    print(l)
    name = multiprocessing.current_process().name
    browser.get(l)
    sleep(4)
    parametrs = []

    f_soup = BS(browser.page_source, 'lxml')

    try:
        phone_buttom = browser.find_element(by.CLASS_NAME, 'mav-hqd3wt').click()
        sleep(3)
        soup = BS(browser.page_source, 'lxml')
        try:
            phone_number = soup.find('div', id = 'modal').find('span', class_ = 'Y2vZ1').text
        except:
            phone_buttom = browser.find_element(by.CLASS_NAME, 'mav-hqd3wt').click()
            sleep(3)
            soup = BS(browser.page_source, 'lxml')
            phone_number = soup.find('div', id='modal').find('span', class_='Y2vZ1').text
        if phone_number in cash:
            # print(phone_number)
            return 0
        else:
            parametrs.append(phone_number)
            cash.append(phone_number)
    except:
        return 0
    try:
        public_data = f_soup.find('div', class_='vvaS4').find('span', class_='YyKdk').text

        if public_data.find('Вчера') != -1:
            today = datetime.datetime.today()
            public_data = today.day - 1
            public_data = datetime.date(today.year, today.month, public_data)
        if public_data.find('Сегодня') != -1:
            public_data = datetime.datetime.today()
        parametrs.append(public_data)
    except:
        parametrs.append('-')
    parametrs.append(l.split('_')[-1])
    # print(parametrs[-1])
    parametrs.append(f_soup.find('h1', class_='BRDq8').text)

    try:
        parametrs.append(
            f_soup.find('div', class_='SMN0B').find('div', class_='c6_NT').find('span', class_='KiS4I').text)
    except:
        parametrs.append('-')

    try:
        parametrs.append(f_soup.find('div', class_ = 'mav-1cepbnp').find('div', class_ = 'CyXiR').find('p', class_ = 'mav-1mdz1i7').text)
    except:
        parametrs.append('-')
    try:
        parametrs.append(f_soup.find('span', class_='mav-m6hjvq').text.split('.')[-1])
    except:
        parametrs.append('-')

    try:
        parametrs.append(f_soup.find('span', class_='mav-m6hjvq').find('div', class_='gSORZ').text.split()[0])
    except:
        parametrs.append('-')

    try:
        parametrs.append(f_soup.find('div', class_='DnFJW').text)
    except:
        parametrs.append('-')

    try:
        parametrs.append(f_soup.find('div', class_ = 'Z4GJI').text)
    except:
        parametrs.append('-')

    # print(parametrs[-1])
    parametrs.append(l)
    try:
        parametrs.append(f_soup.find('div', class_='MGnXI').find('span', class_='JVOab').text)
    except:
        parametrs.append('-')

    if name == 'SpawnPoolWorker-1':
        with open('1.json', 'a', encoding='utf8') as fr:
            fr.write(',')
            try:
                fr.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            except:
                return 0

            fr.close()
    if name == 'SpawnPoolWorker-2':
        with open('4.json', 'a', encoding='utf8') as fl:
            fl.write(',')
            try:
                fl.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            except:
                return 0
            fl.close()

    if name == 'SpawnPoolWorker-3':
        with open('5.json', 'a', encoding='utf8') as fp:
            fp.write(',')
            try:
                fp.write(json.dumps({'item' : parametrs}, indent= 4, ensure_ascii= False))
            except:
                return 0
            fp.close()

    # write_in_excel(parametrs, k)

    # print(phone_number, id, public_data,  name_ad, price, contact_user, address, metro, desciption, l, terms)
    sleep(1.5)


def get_links(url):
    # req = requests.get(url, headers = headers)

    browser.get(url)
    sleep(5)

    # with open('10.html', 'w', encoding='utf8') as file:
    #     file.write(browser.page_source)
    soup = BS(browser.page_source, 'lxml')

    try:
        pages = soup.find('div', class_ = 'index-content-_KxNP').find('div', class_ = 'pagination-hidden-zHaij').find_all('a')
    except:
        pages = [url]
    # print(pages)

    k = 0
    # count = 1
    for page in pages:
        if k != 0:
            page_link = 'https://www.avito.ru' + page.get('href')
            browser.get(page_link)
            soup = BS(browser.page_source, 'lxml')
        else:
            k+=1
        try:
            items_block = soup.find('div', class_ = 'items-items-kAJAg')
            link_blocks = items_block.find_all('div', class_ = 'iva-item-root-_lk9K')
            if link_blocks == []:
                return 0
        except:
            link_blocks = []
            print('No ads')
            break

        for link in link_blocks:
            link_url = 'https://www.avito.ru' + link.find('div', class_ = 'iva-item-body-KLUuy').find('a').get('href') + '\n'
            print(link_url)
            # count+=1
            if link_url not in cash:
                with open('link_url_avito', 'a', encoding='utf8') as f:
                    f.writelines(link_url)
                cash.append(link_url)
            else:
                continue


if __name__ == '__main__':
    # with open('links.txt', 'r', encoding='utf8') as file:
    #     for i in range(43):
    #         l = file.readline().split()
    #         # print(l)
    #         search_word = '+'.join(l)
    #         print(search_word)
    #         # if i < 5:
    #         #     continue
    #         url = f'https://www.avito.ru/moskva_i_mo/vakansii?q={search_word}'
    #         get_links(url)
    #
    # with multiprocessing.Pool(2) as p:
    #     with open('links_delta', 'r', encoding='utf8') as file:
    #         r = file.read().split('\n')
    #         # print(r)
    #         p.map(get_data, r)
    #         p.close()
    #         p.join()
    # get_data()
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
    k = 3302
    # print(data)
    # a = []
    for p in data1:
        # print(p)
        # a.append(p['item'][-2])
        if (p['item'][0][3:6:] == '495') or (p['item'][0][3:6:] == '800'):
            continue
        write_in_excel(p['item'], k)
        print(k)
        k+=1
    for l in data2:
        try:
            # a.append(l['item'][-2])
            # print(p)
            if (l['item'][0][3:6:] == '495') or (l['item'][0][3:6:] == '800'):
                continue
            write_in_excel(l['item'], k)
            print(k)
            k+=1
        except:
            print(k, 'error')
            continue
    # for f in data3:
    #         try:
    #             # a.append(f['item'][-2])
    #             # print(p)
    #             if (l['item'][0][3:6:] == '495') or (l['item'][0][3:6:] == '800'):
    #                 continue
    #             write_in_excel(l['item'], k)
    #             print(k)
    #             k+=1
    #         except:
    #             print(k, 'error')
    #             continue

    # with open('phone_numbers', 'r', encoding='utf8') as op:
    #     for i in range(1348):
    #         c = op.readline()
    #         c.replace('\n', '')
    #         a.append(c)
    #
    # print(a)
    # delta = []
    # with open('link_url_2', 'r', encoding='utf8') as file:
    #     for i in range(7931):
    #         r = file.readline().strip()
            # u = r.split('_')[-1]
            # u.strip()
            # print(u)
            # if r not in a:
            #     r = r+ '\n'
            #     with open('links_delta', 'a', encoding='utf8') as pi:
                    # pi.writelines(r)



    book.save('Avito2.xlsx')









