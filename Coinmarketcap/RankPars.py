from bs4 import BeautifulSoup as BS
import requests
import time
import csv

k = 1
headers = {
    'user-agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
    'accept': '*/*'
}


main_url = 'https://coinmarketcap.com'
for i in range(1,101):
    url = main_url + f'/?page={i}'
    # print(url)
    r = requests.get(url, headers=headers)
    html = r.text

    # with open('crypto_html.html', 'w', encoding='utf-8') as file:
    #     file.write(html)

    soup = BS(html, 'lxml')

    tbody_tr = soup.find('table', class_='cmc-table').find('tbody').find_all('tr')

    for tr in tbody_tr:
        if k < 4126:
            k += 1
            print(k)
            continue
        crypto_link = tr.find('a', class_='cmc-link')
        link = main_url + crypto_link.get('href')

        print(link)
        header = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.366',
            'accept': '*/*'
        }

        # Сделаем Гет запрос для мобильной версии сайта
        r = requests.get(link, headers=header)
        time.sleep(0.5)
        src = r.text
        soup = BS(src, 'lxml')

        content_links = soup.find('div', class_='kHmOmq').find_all('a', class_='modalLink')
        tlg_link = '-'
        rank_number = soup.find('div', class_='nameSection').find('div', class_='namePillPrimary').text
        for part in content_links:
            link_content = part.get('href')
            if part.text == 'Chat' and link_content[0:9:] == 'https://t':
                tlg_link = link_content
        # print(content_links)
        try:
            project_link = content_links[0].get('href')
            crypto_name = soup.find('div', class_='priceSection').find('h1').text.split('Price')[0].strip()
        except:
            project_link = '-'
            crypto_name = '-'
            print(crypto_name, rank_number, tlg_link, project_link)
            with open('Coinmarketcap.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (crypto_name, rank_number, tlg_link, project_link)
                )

        # print(crypto_name)

        print(crypto_name, rank_number, tlg_link, project_link)
        with open('Coinmarketcap.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (crypto_name, rank_number, tlg_link, project_link)
            )
        k += 1
    if i > 41:
        print(i)
        time.sleep(5)