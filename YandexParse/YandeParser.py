from bs4 import BeautifulSoup
import openpyxl
import random
from selenium import webdriver
import time
import random

#Create work-book
book = openpyxl.Workbook()
sheet = book.active

cell_count = 2

sheet['A1'] = 'Заголовок'
sheet['B1'] = 'Местоположение'
sheet['C1'] = 'Цена'
sheet['D1'] = 'Цена за м^2'

class YandexParser():

    def __init__(self):
        self.browser = webdriver.Chrome('chromedriver')

    def close_browser(self):
        self.browser.close()

    def YandexSite(self, n):
        browser = self.browser
        browser.get(f'https://realty.yandex.ru/moskva/kupit/kvartira/dvuhkomnatnaya/?page={n}')
        time.sleep(6)
        html = browser.page_source

        with open('first.html', 'w', encoding= 'utf-8') as file:
            file.write(html)

    def get_data_immovables(self, cell_count):
        with open('first.html', 'r', encoding= 'utf-8') as file:
            src = file.read()
            # print(src)

            soup = BeautifulSoup(src, 'lxml')

            li_immovables = soup.find('ol', class_ = 'OffersSerp__list').find_all('li', class_ = 'OffersSerpItem')
            headers = []
            prices_for_metr = []
            addreses = []
            prices = []
            prices_for_metr = []


            for immovables in li_immovables:
                header = immovables.find('span', class_ = 'OffersSerpItem__title').text
                address_immovables = immovables.find(class_ = 'OffersSerpItem__address').text
                price_immovables = immovables.find('span', class_ = 'price').text
                price_for_metr = immovables.find(class_ = 'OffersSerpItem__price-detail').text
                ''.join(price_for_metr.split('xa'))

                headers.append(header)
                addreses.append(address_immovables)
                prices.append(price_immovables)
                prices_for_metr.append(price_for_metr)

                sheet[f'A{cell_count}'] = header
                sheet[f'B{cell_count}'] = address_immovables
                sheet[f'C{cell_count}'] = price_immovables
                sheet[f'D{cell_count}'] = price_for_metr
                cell_count += 1
            return cell_count





Pars = YandexParser()
# print('Заголовок', 'Местоположение', "Цена", "Цена за метр")
k = 2
for n in range(0, 6):
    Pars.YandexSite(n)
    k = Pars.get_data_immovables(k)
    time.sleep(random.randrange(5,10))
    # break
book.save('YandexImmovablesData.xlsx')
Pars.close_browser()



