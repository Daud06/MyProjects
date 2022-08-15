from bs4 import BeautifulSoup as BS
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By as by
import time
import openpyxl
Param = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}


def collect_data():
    pass

def get_links(url, src, i):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path='C:/Users/Дауд/PycharmProjects/untitled/chromedriver',options=options)

    browser.get(url)
    time.sleep(2)
    src = browser.page_source
    soup = BS(src, 'lxml')

    vacansies_block = soup.find('div', id = 'a11y-main-content').find_all('div', class_ = 'serp-item')
    # print(vacansies_block)

    i = 2
    for block in vacansies_block:
        telephone = '-'
        browser.find_element(by.XPATH, f'/html/body/div[5]/div/div[3]/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/div[{i}]/div/div[4]/button').click()

        time.sleep(10)
        with open('../43.html', 'w', encoding='utf-8') as file:
            file.write(browser.page_source)
            file.close
        # telephone = browser.find_element(by.XPATH, '/html/body/div[12]/div/div[1]/div/div[2]').text
        # print(telephone)

        break
        vacansies_id= block.find('h3', class_ = 'bloko-header-section-3').find('a').get('href').split('/')[4][0:7:]
        print(vacansies_id)
        break

def main(request_words):
    main_url = f'https://hh.ru/search/vacancy?text={request_words}&items_on_page=100&page=0'
    req = requests.get(main_url, headers=Param)
    req.close()
    html = req.text
    soup = BS(html, 'lxml')
    page_count = soup.find('h1').text.split()[0]
    page_count = (int(page_count) // 100) + 1
    print(page_count)
    for i in range(page_count):
        url = f'https://hh.ru/search/vacancy?text={request_words}&items_on_page=100&page={i}'
        get_links(url, html, i)
        break


if __name__ == '__main__':
    with open('../search_data.txt', 'r', encoding='utf-8') as file:
        for i in range(43):
            l = file.readline().split()
            # print('+'.join(l))
            main('+'.join(l))
            break