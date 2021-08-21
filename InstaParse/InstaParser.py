from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import time
import random

username = 'web.programmist'
password = 'ahriev06'


class InstaBot():

    def __init__(self, password, username):
        self.password = password
        self.username = username
        self.browser = webdriver.Chrome('chromedriver')

    def browser_close(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(1,5))

        username_input = browser.find_elements_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_elements_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(15)


bot = InstaBot(password, username)

bot.login()
bot.browser_close()


