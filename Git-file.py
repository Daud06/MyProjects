import requests
from bs4 import BeautifulSoup as BS
# import lxml
import json
import openpyxl
import csv


#Create work-book
book = openpyxl.Workbook()
sheet = book.active

cell_count = 2

sheet['A1'] = 'Название криптовалюты'
sheet['B1'] = 'Стоимость'
sheet['C1'] = 'Капитализация'
sheet['D1'] = 'Изменение за 24 часа'



crypto = []
for count in range(1, 4):

    url = f'https://myfin.by/crypto-rates?page={count}'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    r = requests.get(url, headers = headers)
    html = r.text

    soup = BS(html, 'lxml')
    all_crypto = soup.find('tbody', class_ = 'table-body').find_all('tr')

    for item in all_crypto:

        crypto_name = item.find(class_ = 'names').find('a').text
        crypto_price = item.find_next('td').find_next('td').get_text().split()[0]
        change = item.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find('span').text
        crypto_capital = item.find_next('td').find_next('td').find_next('td').get_text()
        crypto.append(
            (
                crypto_name,
                crypto_price,
                crypto_capital,
                change
            )
        )
        sheet[f'A{cell_count}'] = crypto_name
        sheet[f'B{cell_count}'] = crypto_price
        sheet[f'C{cell_count}'] = crypto_capital
        sheet[f'D{cell_count}'] = change

        # with open('crypto_values.csv', 'a') as file:
        #     writer = csv.writer(file)
        #     writer.writerow(
        #         [
        #             crypto_name,
        #             crypto_price,
        #             crypto_capital,
        #             change
        #          ]
        #     )
        cell_count += 1

# with open("all_categories_dict.json", "w") as file:
    # json.dump(crypto, file, indent=4, ensure_ascii=False)






book.save('crypto_values.xlsx')






