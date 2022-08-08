from bs4 import BeautifulSoup as BS
import time
from selenium import webdriver
from selenium.webdriver.common.by import By as by
import random
from auth_data import password, username
import csv
from selenium.webdriver.common.keys import Keys

# with open('GameParse.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(
#         ('App name', 'Revenue', 'US percent of revenue', 'Downloads', 'US percent of downloads')
#     )

class GameParse():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.browser =  webdriver.Chrome(executable_path='C:/Users/Дауд/PycharmProjects/untitled/chromedriver', options = options)

    def auth_func(self, url, password, username):
        browser = self.browser
        browser.get(url)
        time.sleep(7)
        log_in_buttom = browser.find_element(by.XPATH, '/html/body/app-root/layout/div[1]/div/auth/button').click()
        time.sleep(random.randrange(1,6))
        privacy_accept = browser.find_element(by.XPATH, '/html/body/div[4]/div/login-dialog/div/div/login/div[2]/div[2]/div/div[1]/div[1]/am-checkbox/div').click()
        time.sleep(2)
        Kakao_auth = browser.find_element(by.XPATH, '/html/body/div[4]/div/login-dialog/div/div/login/div[2]/div[2]/div/div[1]/div[6]').click()
        time.sleep(10)
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(10)

        username_input = browser.find_element(by.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/form/fieldset/div[2]/div/input')
        username_input.clear()
        username_input.send_keys(username)
        time.sleep(random.randrange(3, 7))
        password_input = browser.find_element(by.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/form/fieldset/div[3]/input')
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(random.randrange(2,5))
        put_buttom_log = browser.find_element(by.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div[2]/div/form/fieldset/div[8]/button[1]').click()
        time.sleep(10)

        browser.switch_to.window(browser.window_handles[0])
        time.sleep(2)
        browser.get('https://appmagic.rocks/top-charts/apps?topDepth=1000')
        time.sleep(30)
        html = browser.page_source
        with open('1000.html', 'w', encoding='utf-8') as file:
            file.write(html)

    def browser_close(self):
        browser = self.browser
        browser.close()
        browser.quit()


    def get_data_games(self, url):

        browser = self.browser

        with open('1000.html', 'r', encoding='utf-8') as file:
            src = file.read()
            # print(src)
            soup = BS(src, 'lxml')

            top_apps = soup.find('top-rows-wrap').find_all('app-list-item', class_ = 'parent-app-info-hover')

        # print(top_apps)
        i = 1
        t = 6
        app_links = []
        for app in top_apps:
            if i <= 896:
                i+=1
                continue
            app_name = app.find('a', class_ = 'g-app-name').text
            app_link = 'https://appmagic.rocks/' + app.find('a', class_ = 'g-app-name').get('href')

            # print(app_link)
            browser.get(app_link)

            if i % 30 == 0 and t!=10:
                t+=0.5


            time.sleep(t)
            html = browser.page_source

            soup_link = BS(html, 'lxml')

            """
            Загоним следующую часть кода под try т.к попадаются страницы, на которых информация о revenue или downloads(или и том, и о 
            другом) за последние 30 дней отсутсвует. Элементы блоков взаимосвязаны и информацию о 2ом блоке с downloads нужно искать 
            отталкиваясь от эл-ов 1го блока
            """
            try:
                count_revenue = soup_link.find('div', class_ = 'head-wrap').find('span', class_ = 'label').text
                revenue_block = soup_link.find('horizontal-stats', class_ = 'ng-star-inserted')

                #Проверяем существует ли блок с downloads при условии существования блока с revenue
                try:
                    count_downloads = soup_link.find('div', class_ = 'head-wrap').find_next('div', class_ = 'head-wrap').find('span', class_ = 'label').text
                    download_block = soup_link.find('horizontal-stats', class_='ng-star-inserted').find_next('horizontal-stats', class_='ng-star-inserted')
                except:
                    count_downloads = '-'
                    download_block = '-'


                if revenue_block.text.count('United States') != 0:

                    countries = revenue_block.find_all('div', class_ = 'stats-label')
                    ctr_percents = revenue_block.find_all('div', class_ = 'percent')
                    k = 0
                    for country in countries:
                        c = country.text.strip()
                        if c == 'United States':
                            revenue_index = k
                            revenue_percent = ctr_percents[revenue_index].text
                        k+=1
                else:
                    revenue_percent = '-'
            except:
                count_revenue = '-'
                revenue_percent = '-'
                """
                Если информации о revenue нет, то ставим "-" в соответствующих переменных и проверям на наличие информации 
                2-ой блок  
                """
                try:
                    count_downloads = soup_link.find('span', class_ = 'label').text
                    download_block = soup_link.find('horizontal-stats', class_='ng-star-inserted')
                except:
                    count_downloads = '-'
                    download_block = ''
                    with open('GameParse.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (app_name, count_revenue, revenue_percent, count_downloads, dwn_percent)
                        )
                    continue

            if download_block.text.count('United States') != 0:

                # print(revenue_block.text.find('United States'))
                countries_download = download_block.find_all('div', class_ = 'stats-label')
                ctr_percents_download = download_block.find_all('div', class_ = 'percent')
                k = 0
                for country_dwn in countries_download:
                    dwn = country_dwn.text.strip()
                    if dwn == 'United States':
                        download_index = k
                        # country_dwn = dwn
                        dwn_percent = ctr_percents_download[download_index].text
                        # print(country_dwn, dwn_percent)
                    k+=1
            else:
                dwn_percent = '-'

            print(app_name, count_revenue , revenue_percent, count_downloads, dwn_percent)
            with open('GameParse.csv', 'a', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (app_name, count_revenue , revenue_percent, count_downloads, dwn_percent)
                )


            i+=1
            if i % 50 == 0:
                # screen_unsleep = browser.find_element(by.XPATH, '/html/body/app-root/layout/div[2]/app-page/app-info-dialog/div[1]/div[1]/div[1]/div[2]/div[1]/div').click()
                time.sleep(15)
            if i == 1001:
                break



        # time.sleep(10)



url = 'https://appmagic.rocks/top-charts/apps'

Parser = GameParse()

file = open('1000.html', 'r', encoding='utf-8')
r = file.read()
if r == '':
    Parser.auth_func(url, password, username)
Parser.get_data_games('https://appmagic.rocks/top-charts/apps?topDepth=1000')
Parser.browser_close()