from selenium import webdriver
import requests
from selenium.webdriver.common.keys import Keys
import json
import time
import random
from selenium.common.exceptions import NoSuchElementException

username = ''
password = ''



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

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)


        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def go_to_profile(self):
        browser = self.browser
        browser.get(f'https://www.instagram.com/web.programmist/')
        time.sleep(5)

        #followers = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/ul/li[3]').click()

        #time.sleep(3)
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
            print('way on the element not found')
        return exist
    def full_post(self):
        browser = self.browser

        for i in range(1, 3):
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(4)
        all_links = browser.find_elements_by_tag_name('a')
        post_links = [item.get_attribute('href') for item in all_links if '/p/' in item.get_attribute('href')]
        return post_links


    #Ставить лайки
    def put_like(self):
        browser = self.browser
        post_links = self.full_post()
        post_links = post_links[::-1]
        for i in post_links:
            print(i)
        # print(post_links)
        for url in post_links:
            browser.get(url)
            like_buttom = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/span[1]/button')
            like_buttom.click()

            time.sleep(4)
            break

    #Удалить пост
    def delete_post(self):

        browser = self.browser

        post_links = self.full_post()
        # post_links = post_links[::-1]
        count = 6
        for url in post_links:
            browser.get(url)
            menu_buttom = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/div/button').click()
            # presention_div = browser.find_element_by_class_name('RnEpo Yx5HN      ')
            time.sleep(5)
            delete_buttom = browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div/button[1]').click()
            time.sleep(5)
            confirm_delete = browser.find_element_by_xpath('/html/body/div[6]/div/div/div/div[2]/button[1]').click()
            time.sleep(20)
            count -= 1
            if count == 0:
                post_links = self.full_post()
                count = 6

    def unsubscribing_from_users(self):
        browser = self.browser

        subscribe_count = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text
        subscribe_count = int(subscribe_count)
       # all_subscribe.click()
        print(subscribe_count)
        time.sleep(4)
        #subscribe_count = int(subscribe_count)

        #кол-во перезагрузок
        loops_count = int(subscribe_count / 10) + 1

        for i in range(1, loops_count + 1):
            count = 10
            self.go_to_profile()
            time.sleep(random.randrange(2,4))

            all_subscribe = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]')
            all_subscribe.click()
            time.sleep(random.randrange(3,4))

            all_users_div = browser.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/ul/div')
            all_users = all_users_div.find_elements_by_tag_name('li')
            # print(all_users)
            for item in all_users:
                if count == 0:
                    break
                users_button = item.find_element_by_tag_name('button')
                users_button.click()
                time.sleep(2)
                confirm_buttom = item.find_element_by_xpath('/html/body/div[7]/div/div/div/div[3]/button[1]').click()
                subscribe_count -= 1
                print(subscribe_count)
                time.sleep(25)
                count -= 1






bot = InstaBot(password, username)

bot.login()
bot.go_to_profile()
# bot.put_like()
# bot.unsubscribing_from_users()
bot.browser_close()



