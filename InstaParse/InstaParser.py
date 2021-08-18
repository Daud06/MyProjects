from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time


username = 'daud_ahr'
password = 'ahriev06'

url = 'https://www.instagram.com/'

def login(username, password):
    browser = webdriver.Chrome('chromedriver')
    try:
        browser.get(url)
        time.sleep(random.randrange(3,5))

        username_input = browser.find_element_by_name('username')
        username_input.send_keys(username)

        time.sleep(3)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)


        password_input.send_keys(Keys.ENTER)

        browser.close()
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

login(username, password)


