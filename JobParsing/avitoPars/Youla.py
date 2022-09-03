from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By as by
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path='C:/Users/Дауд/PycharmProjects/untitled/chromedriver', options = options)
cash = []

def get_data():

    with open('link_url', 'r', encoding='utf8') as file:
        for i in range(1087):
            l = file.readline()
            l = l.replace('/moskva/', '/')
            browser.get(l)
            sleep(1000)




def get_links(url):
    browser.get(url)
    sleep(3)

    page_end_text = ' '
    p = 0
    scroll_count_last = 0
    scroll_count = 650
    ad_count = 0

    try:
        stop_text = browser.find_element(by.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div/section/div[4]/div[2]/div/div[3]/div[2]/p[1]').text
        return 0
    except:
        pass

    while page_end_text!= 'Измените условия поиска, чтобы увидеть больше товаров':

        html = browser.page_source
        soup = BS(html, 'lxml')

        link_block = soup.find('div', class_ = 'dUJlcF')
        # print(link_block)

        links = link_block.find_all('div', class_ = 'hKoGOf')

        # print(links[2])
        # print(links)
        # with open('10.html', 'w', encoding='utf8') as f:
        #     f.write(html)
        main_url = 'https://youla.ru/moskva'
        # return 0
        for link in links[p:p+8]:
            # print(link)
            try:
                link_url = main_url + link.find('a').get('href') + '\n'
                print(link_url)
                if link_url not in cash:
                    with open('link_url', 'a', encoding='utf8') as f:
                            f.writelines(link_url)
                    cash.append(link_url)
                else:
                    ad_count+=1
                    continue
            except:
                print('error')
                ad_count+=1
                continue
            ad_count+=1
            print(ad_count)
        browser.execute_script(f'window.scrollTo({scroll_count_last}, {scroll_count})')
        sleep(4)
        scroll_count_last = scroll_count
        scroll_count += 640
        p += 8
        links_count = len(links)

        if ad_count == links_count:
            page_end_text = browser.find_element(by.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/section/div[4]/div[2]/div/div[3]').text

            # print(page_end_text)

if __name__ == '__main__':

    # with open('links.txt', 'r', encoding='utf8') as file:
    #     for i in range(43):
    #         l = file.readline()
    #         print(l)
    #         if i < 9:
    #             continue
    #         url = f'https://youla.ru/moskva/rabota?q={l}'
    #         # get_links(url)
    get_data()