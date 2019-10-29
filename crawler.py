#Copyrightⓒ2019 Lee Jin Woo All rights reserved.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains


from pymongo import MongoClient

from bs4 import BeautifulSoup

import time
import random
import sys
import csv
import asyncio

def give_me_the_number_divided_two(keywords):
    return int(len(keywords) / 2)

def first_keywords_part(keywords_number, keywords):
    return keywords[0:keywords_number]
    
def second_keywords_part(keywords_number, keywords):
    return keywords[keywords_number:]


###Smart Store 배열을 2개로 나누어 진행하기
def split_two_list(keywords, shoppingUrl):
    the_number_of_keywords_divided_two = int(len(keywords) / 2)
    keywords_one = keywords[0:the_number_of_keywords_divided_two]
    keywords_two = keywords[the_number_of_keywords_divided_two:]

    tmp_keywords_one = []
    tmp_keywords_two = []

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
    #first smart store number가 3을 넘을시 시간차를 두고 다시 들어가서 크롤링
    first_smart_store_number = 0
    #First Keywords List
    for keyword_one in keywords_one:
        #first_smart_store_number가 3이하일시 실행
        if first_smart_store_number < 3:
            # shopping page로 이동

            driver.get(shoppingUrl)
            time.sleep(random.randint(5, 7))

            # 검색어에 keyword_one을 입력하고 enter버튼 누르기
            try:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            except:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
                
                
            # 검색된 결과에서 물건의 갯수를 크롤링
            try:
                time.sleep(random.randint(7,9))
                products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
            #실패시 다시
            except NoSuchElementException:
                try:
                    driver.refresh()
                    time.sleep(random.randint(4, 7))
                    products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
                #실패시 다시 끄고 keyword입력해서 다시
                except NoSuchElementException:

                    try:
                        driver.quit()
                        options = webdriver.ChromeOptions()
                        options.add_argument('--headless')
                        driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
                        driver.get(shoppingUrl)
                        time.sleep(random.randint(5, 7))
            
                        try:
                            driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                            ActionChains(driver).send_keys(Keys.RETURN).perform()
                        except:
                            driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                            ActionChains(driver).send_keys(Keys.RETURN).perform()
                        time.sleep(random.randint(5, 10))
                        products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
                    except NoSuchElementException:
                        tmp_keywords_one.append(0)
                    else:
                        products_string_type = products_string_type.text
                        if '전체' in products_string_type:
                            products_string_type = products_string_type.replace('전체', '')
                        if ',' in products_string_type:
                            products_string_type = products_string_type.replace(',', '')
                        #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                        tmp_keywords_one.append(int(products_string_type))


                else:
                    products_string_type = products_string_type.text
                    if '전체' in products_string_type:
                        products_string_type = products_string_type.replace('전체', '')
                    if ',' in products_string_type:
                        products_string_type = products_string_type.replace(',', '')
                    #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                    tmp_keywords_one.append(int(products_string_type))

            else:
                products_string_type = products_string_type.text
                print(products_string_type)
                if '전체' in products_string_type:
                    products_string_type = products_string_type.replace('전체', '')
                if ',' in products_string_type:
                    products_string_type = products_string_type.replace(',', '')
                #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                tmp_keywords_one.append(int(products_string_type))

            first_smart_store_number = first_smart_store_number + 1
            print(tmp_keywords_one)
        
        #first_smart_store_number 가 3을 넘긴 때는 driver를 닫고 다시 열어서 똑같은 방식으로 진행을 한다.
        else:
            #driver 종료
            driver.quit()
            time.sleep(random.randint(4, 7))
            #다시 shopping page로 들어오기
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)

            driver.get(shoppingUrl)
            time.sleep(random.randint(5, 7))
            # 검색어에 keyword_one을 입력하고 enter버튼 누르기
            try:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            except:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            
            
            # 검색된 결과에서 물건의 갯수를 크롤링
            try:
                time.sleep(random.randint(7,9))
                products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
            #실패시 다시
            except NoSuchElementException:
                try:
                    driver.refresh()
                    time.sleep(random.randint(4, 7))
                    products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
                    products_string_type = products_string_type.text

                    if '전체' in products_string_type:
                        products_string_type = products_string_type.replace('전체', '')
                    if ',' in products_string_type:
                        products_string_type = products_string_type.replace(',', '')
                    #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                    tmp_keywords_one.append(int(products_string_type))
                #물건이 없거나 page오류이므로 두가지 경우를 모두 처리
                except Exception:
                    try:
                        driver.quit()
                        time.sleep(random.randint(5, 10))
                        options = webdriver.ChromeOptions()
                        options.add_argument('--headless')
                        driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
                        driver.get(shoppingUrl)
                        time.sleep(random.randint(5, 7))
                        try:
                            driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                            ActionChains(driver).send_keys(Keys.RETURN).perform()
                        except:
                            driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                            ActionChains(driver).send_keys(Keys.RETURN).perform()
                        time.sleep(random.randint(5, 10))
                        products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
                    except NoSuchElementException:
                        tmp_keywords_one.append(0)
                    else:
                        products_string_type = products_string_type.text
                        if '전체' in products_string_type:
                            products_string_type = products_string_type.replace('전체', '')
                        if ',' in products_string_type:
                            products_string_type = products_string_type.replace(',', '')
                        #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                        tmp_keywords_one.append(int(products_string_type))

            else:
                products_string_type = products_string_type.text
                print(products_string_type)
                if '전체' in products_string_type:
                    products_string_type = products_string_type.replace('전체', '')
                if ',' in products_string_type:
                    products_string_type = products_string_type.replace(',', '')
                #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                tmp_keywords_one.append(int(products_string_type))

            first_smart_store_number = first_smart_store_number + 1
            print(tmp_keywords_one)
            
    #first list driver 종료
    driver.quit()

    time.sleep(random.randint(10, 15))

    second_smart_store_number = 0
    #Second Keywords List
    for keyword_two in keywords_two:
        if second_smart_store_number < 3:
            # shopping page로 이동

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
            
            driver.get(shoppingUrl)
            time.sleep(random.randint(5, 7))
            # 검색어에 keyword_one을 입력하고 enter버튼 누르기
            try:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_two)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            except:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_two)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            time.sleep(random.randint(7, 9))
            
            # 검색된 결과에서 물건의 갯수를 크롤링
            try:
                time.sleep(random.randint(7,9))
                products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
            #실패시 다시
            except NoSuchElementException:

                try:
                    driver.quit()
                    time.sleep(random.randint(5, 10))
                    options = webdriver.ChromeOptions()
                    options.add_argument('--headless')
                    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
                    driver.get(shoppingUrl)
                    time.sleep(random.randint(5, 7))
                    try:
                        driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                        ActionChains(driver).send_keys(Keys.RETURN).perform()
                    except:
                        driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                        ActionChains(driver).send_keys(Keys.RETURN).perform()
                        
                    time.sleep(random.randint(5, 10))
                    products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')

                except NoSuchElementException:
                    tmp_keywords_two.append(0)
                else:
                    products_string_type = products_string_type.text
                    if '전체' in products_string_type:
                        products_string_type = products_string_type.replace('전체', '')
                    if ',' in products_string_type:
                        products_string_type = products_string_type.replace(',', '')
                    #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                    tmp_keywords_two.append(int(products_string_type))


            else:
                products_string_type = products_string_type.text
                print(products_string_type)
                if '전체' in products_string_type:
                    products_string_type = products_string_type.replace('전체', '')
                if ',' in products_string_type:
                    products_string_type = products_string_type.replace(',', '')
                #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                tmp_keywords_two.append(int(products_string_type))

            second_smart_store_number = second_smart_store_number + 1
            print(tmp_keywords_two)
        
        #first_smart_store_number 가 3을 넘긴 때는 driver를 닫고 다시 열어서 똑같은 방식으로 진행을 한다.
        else:
            #driver 종료
            driver.quit()
            time.sleep(random.randint(4, 6))
            #다시 shopping page로 들어오기
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')

            driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)

            driver.get(shoppingUrl)
            time.sleep(random.randint(5, 7))
            # 검색어에 keyword_one을 입력하고 enter버튼 누르기
            try:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_two)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            except:
                driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_two)
                ActionChains(driver).send_keys(Keys.RETURN).perform()
            time.sleep(random.randint(7, 9))
            
            # 검색된 결과에서 물건의 갯수를 크롤링
            try:
                time.sleep(random.randint(7,9))
                products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
            #실패시 다시
            except NoSuchElementException:

                try:
                    driver.quit()
                    time.sleep(random.randint(5, 10))
                    options = webdriver.ChromeOptions()
                    options.add_argument('--headless')
                    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
                    driver.get(shoppingUrl)
                    time.sleep(random.randint(5, 7))
                    try:
                        driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                        ActionChains(driver).send_keys(Keys.RETURN).perform()
                    except:
                        driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(keyword_one)
                        ActionChains(driver).send_keys(Keys.RETURN).perform()
                    time.sleep(random.randint(5, 10))
                    products_string_type = driver.find_element_by_xpath('//*[@id="snb"]/ul/li[1]/a')
                except NoSuchElementException:
                    tmp_keywords_two.append(0)
                else:
                    products_string_type = products_string_type.text
                    if '전체' in products_string_type:
                        products_string_type = products_string_type.replace('전체', '')
                    if ',' in products_string_type:
                        products_string_type = products_string_type.replace(',', '')
                    #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                    tmp_keywords_two.append(int(products_string_type))

            else:
                products_string_type = products_string_type.text
                print(products_string_type)
                if '전체' in products_string_type:
                    products_string_type = products_string_type.replace('전체', '')
                if ',' in products_string_type:
                    products_string_type = products_string_type.replace(',', '')
                #필요없는 숫자들 제거후 tmp_keywords_one 에 저장
                tmp_keywords_two.append(int(products_string_type))

            second_smart_store_number = second_smart_store_number + 1
            print(tmp_keywords_two)

    #Second Driver 종료
    driver.quit()
    result_keywords = tmp_keywords_one + tmp_keywords_two
    return result_keywords


class Crawler:
    def __init__(self, naver_id, naver_password):

        self.naver_id = naver_id
        self.naver_password = naver_password
        self.keywords_name = []
        self.keywords_pc_search = []
        self.keywords_phone_search = []
        self.cafe_contents = []
        self.blog_contents = []
        self.smart_store_products = []
        self.keywords = []

    def check_not_abandoned_keyword_in_naver(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        baseUrl = 'https://searchad.naver.com'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(baseUrl)
        driver.implicitly_wait(5)

        #id, password 입력하기

        driver.find_element_by_xpath('//*[@id="uid"]').send_keys(self.naver_id)
        driver.implicitly_wait(random.randint(2,4))
        driver.find_element_by_xpath('//*[@id="upw"]').send_keys(self.naver_password)
        driver.implicitly_wait(random.randint(2,4))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        #naver 키워드 도구로 이동
        driver.implicitly_wait(2)

        driver.get('https://manage.searchad.naver.com/front')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        driver.implicitly_wait(5)

        #keyword 사용자에게 입력받기
        keyword_candidate_one = keyword1
        keyword_candidate_two = keyword2
        keyword_candidate_three = keyword3
        keyword_candidate_four = keyword4
        keyword_candidate_five = keyword5

        driver.implicitly_wait(random.randint(3,5))

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_one)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_two)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_three)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_four)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_five)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button').click()

        driver.implicitly_wait(random.randint(3,5))

        try:
            driver.find_element_by_xpath('//*[@id="toast-container"]/div')
            print('[-] Abandoned Keyword exists...')
            driver.quit()
            return False
        except NoSuchElementException as e:
            print('[+]Safe Keywords In There... {}'.format(e))
            driver.quit()
            return True
        

    #Login Naver Ad

    #인기있는 키워드 200개 추출
    def login_naver_ad_200_popular(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        baseUrl = 'https://searchad.naver.com'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(baseUrl)
        driver.implicitly_wait(5)

        #id, password 입력하기

        driver.find_element_by_xpath('//*[@id="uid"]').send_keys(self.naver_id)
        driver.implicitly_wait(random.randint(2,4))
        driver.find_element_by_xpath('//*[@id="upw"]').send_keys(self.naver_password)
        driver.implicitly_wait(random.randint(2,4))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        #naver 키워드 도구로 이동
        driver.implicitly_wait(2)

        driver.get('https://manage.searchad.naver.com/front')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        driver.implicitly_wait(5)

        #keyword 사용자에게 입력받기
        keyword_candidate_one = keyword1
        keyword_candidate_two = keyword2
        keyword_candidate_three = keyword3
        keyword_candidate_four = keyword4
        keyword_candidate_five = keyword5

        driver.implicitly_wait(random.randint(3,5))

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_one)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_two)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_three)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_four)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_five)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button').click()

        driver.implicitly_wait(random.randint(3,5))

        #금지된 키워드가 들어가 있을경우 No!
        try:
            if driver.find_element_by_xpath('//*[@id="toast-container"]/div'):
                print('[-] Abandoned Keyword Exists')
                driver.quit()
                return False
        #금지된 키워드가 없는경우
        except NoSuchElementException as e:
            time.sleep(3)
            #pageSource가지고 오기
            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, 'html.parser')

            #항목의 수
            a_length = len(bs.findAll('a', {'class': 'page-link'}))

            if a_length <= 5:
                print('Small Size!')
                time.sleep(3)
                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                #keyword name 검색결과 저장
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)
                        
                #키워드 클릭해서 동향 알아보기
                        
                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(',', '')
                    if '<' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace('<', '')
                    if ' ' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_click))

                    
                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                    keyword_phone_click = str(keyword_phone_tag.get_text())

                #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(',', '')
                    if '<' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace('<', '')
                    if ' ' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(' ', '')

                    #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_click))

            else:
                for link_number in range(3, 5):
                    time.sleep(3)
                    
                    #고친부분
                    pageSource = driver.page_source
                    bs = BeautifulSoup(pageSource, 'html.parser')

                    #keyword name 검색결과 저장
                    for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                        keyword_name = keyword_name_tag.get_text()
                        self.keywords_name.append(keyword_name)
                        
                    #키워드 클릭해서 동향 알아보기
                        
                    #고친부분

                    #keyword pc click 검색결과 저장
                    for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                        keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                        #keyword_pc_click 에서 쓸모없는부분 제거
                        if ',' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(',', '')
                        if '<' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace('<', '')
                        if ' ' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                        #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                        self.keywords_pc_search.append(int(keyword_pc_click))

                    
                    #keyword phone click 검색결과 저장
                    for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                        keyword_phone_click = str(keyword_phone_tag.get_text())

                        #keyword_phone_click 에서 쓸모없는부분 제거
                        if ',' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(',', '')
                        if '<' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace('<', '')
                        if ' ' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(' ', '')
                        #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                        self.keywords_phone_search.append(int(keyword_phone_click))

                    
                    #다음페이지 click
                    driver.find_elements_by_class_name('page-item')[link_number].click()
        driver.quit()
        return True

    #인기없는 키워드 200개 추출

    def login_naver_ad_200_unpopular(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        baseUrl = 'https://searchad.naver.com'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(baseUrl)
        driver.implicitly_wait(5)

        #id, password 입력하기

        driver.find_element_by_xpath('//*[@id="uid"]').send_keys(self.naver_id)
        driver.implicitly_wait(random.randint(2,4))
        driver.find_element_by_xpath('//*[@id="upw"]').send_keys(self.naver_password)
        driver.implicitly_wait(random.randint(2,4))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        #naver 키워드 도구로 이동
        driver.implicitly_wait(2)

        driver.get('https://manage.searchad.naver.com/front')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        driver.implicitly_wait(5)

        #keyword 사용자에게 입력받기
        keyword_candidate_one = keyword1
        keyword_candidate_two = keyword2
        keyword_candidate_three = keyword3
        keyword_candidate_four = keyword4
        keyword_candidate_five = keyword5

        #먼저 검색한 keyword수 알아내기
        searched_keyword_number = 0

        tmp_keywords = [keyword_candidate_one, keyword_candidate_two, keyword_candidate_three, keyword_candidate_four, keyword_candidate_five]
        for tmp_keyword in tmp_keywords:
            if tmp_keyword is not '':
                searched_keyword_number = searched_keyword_number + 1
        

        driver.implicitly_wait(random.randint(3,5))

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_one)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_two)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_three)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_four)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_five)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button').click()

        driver.implicitly_wait(random.randint(3,5))

        #금지된 키워드가 들어가 있을경우 No!
        try:
            if driver.find_element_by_xpath('//*[@id="toast-container"]/div'):
                print('[-] 금지된 키워드가 존재합니다. 다른 키워드를 입력하여 다시 실행해 주세요!')
                driver.quit()
                return False
        #금지된 키워드가 없는경우
        except NoSuchElementException as e:
            time.sleep(3)

            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, 'html.parser')

            #항목의 수
            a_length = len(bs.findAll('a', {'class': 'page-link'}))

            if a_length <= 5:
                print('Small Size!')
                time.sleep(3)
                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                #keyword name 검색결과 저장
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)
                        
                #키워드 클릭해서 동향 알아보기
                        
                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(',', '')
                    if '<' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace('<', '')
                    if ' ' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_click))

                    
                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                    keyword_phone_click = str(keyword_phone_tag.get_text())

                #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(',', '')
                    if '<' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace('<', '')
                    if ' ' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(' ', '')

                    #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_click))

            else:
                ###처음페이지로 가서 입력한 keyword 따오기

                #검색했던 keyword 정보들을 수집
                tmp_keyword_name_iteration = 0
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    if tmp_keyword_name_iteration == searched_keyword_number:
                        break                
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)
                    tmp_keyword_name_iteration = tmp_keyword_name_iteration + 1

                tmp_keyword_pc_click_iteration = 0
                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    if tmp_keyword_pc_click_iteration == searched_keyword_number:
                        break
                    keyword_pc_click = str(keyword_pc_tag.get_text())
                            
                #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(',', '')
                    if '<' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace('<', '')
                    if ' ' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(' ', '')
                            
                #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_click))

                    tmp_keyword_pc_click_iteration = tmp_keyword_pc_click_iteration + 1

                tmp_keyword_phone_click_iteration = 0

                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                    if tmp_keyword_phone_click_iteration == searched_keyword_number:
                        break

                    keyword_phone_click = str(keyword_phone_tag.get_text())

                #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(',', '')
                    if '<' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace('<', '')
                    if ' ' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(' ', '')

                #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_click))

                    tmp_keyword_phone_click_iteration = tmp_keyword_phone_click_iteration + 1

                ###
                ###인기없는 페이지로 이동
                        #Unpopular 나열
                time.sleep(3)
                driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[2]/div[3]/elena-table/div/div/table/thead/tr[1]/th[6]/elena-basic-column-header/div/span').click()
                driver.implicitly_wait(random.randint(3,5))

                #pageSource가지고 오기
                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                for link_number in range(3, 5):
                    time.sleep(3)
                    
                    #고친부분
                    pageSource = driver.page_source
                    bs = BeautifulSoup(pageSource, 'html.parser')

                    #keyword name 검색결과 저장
                    for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                        keyword_name = keyword_name_tag.get_text()
                        self.keywords_name.append(keyword_name)
                        
                    #키워드 클릭해서 동향 알아보기
                        
                    #고친부분

                    #keyword pc click 검색결과 저장
                    for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                        keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                        #keyword_pc_click 에서 쓸모없는부분 제거
                        if ',' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(',', '')
                        if '<' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace('<', '')
                        if ' ' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                        #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                        self.keywords_pc_search.append(int(keyword_pc_click))

                    
                    #keyword phone click 검색결과 저장
                    for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                        keyword_phone_click = str(keyword_phone_tag.get_text())

                        #keyword_phone_click 에서 쓸모없는부분 제거
                        if ',' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(',', '')
                        if '<' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace('<', '')
                        if ' ' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(' ', '')

                        #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                        self.keywords_phone_search.append(int(keyword_phone_click))

                    
                    #다음페이지 click
                    driver.find_elements_by_class_name('page-item')[link_number].click()
        driver.quit()
        return True

    #그저그런 인기를 가진 keyword 정보 추출
    def login_naver_ad_200_normal(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        baseUrl = 'https://searchad.naver.com'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(baseUrl)
        driver.implicitly_wait(5)

        #id, password 입력하기

        driver.find_element_by_xpath('//*[@id="uid"]').send_keys(self.naver_id)
        driver.implicitly_wait(random.randint(2,4))
        driver.find_element_by_xpath('//*[@id="upw"]').send_keys(self.naver_password)
        driver.implicitly_wait(random.randint(2,4))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        #naver 키워드 도구로 이동
        driver.implicitly_wait(2)

        driver.get('https://manage.searchad.naver.com/front')
        driver.implicitly_wait(5)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()
        driver.implicitly_wait(2)
        driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        driver.implicitly_wait(5)

        #keyword 사용자에게 입력받기
        keyword_candidate_one = keyword1
        keyword_candidate_two = keyword2
        keyword_candidate_three = keyword3
        keyword_candidate_four = keyword4
        keyword_candidate_five = keyword5

        #먼저 검색한 keyword수 알아내기
        searched_keyword_number = 0

        tmp_keywords = [keyword_candidate_one, keyword_candidate_two, keyword_candidate_three, keyword_candidate_four, keyword_candidate_five]
        for tmp_keyword in tmp_keywords:
            if tmp_keyword is not '':
                searched_keyword_number = searched_keyword_number + 1

        driver.implicitly_wait(random.randint(3,5))

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_one)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_two)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_three)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_four)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_five)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button').click()

        driver.implicitly_wait(random.randint(3,5))

        #금지된 키워드가 들어가 있을경우 No!
        try:
            if driver.find_element_by_xpath('//*[@id="toast-container"]/div'):
                print('[-] 금지된 키워드가 존재합니다. 다른 키워드를 입력하여 다시 실행해 주세요!')
                driver.quit()
                return False
        #금지된 키워드가 없는경우
        except NoSuchElementException as e:
            time.sleep(3)

            #pageSource가지고 오기
            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, 'html.parser')

            #항목의 수
            a_length = len(bs.findAll('a', {'class': 'page-link'}))

            if a_length <= 5:
                print('Small Size!')
                time.sleep(3)
                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                #keyword name 검색결과 저장
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)
                        
                #키워드 클릭해서 동향 알아보기
                        
                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(',', '')
                    if '<' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace('<', '')
                    if ' ' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_click))

                    
                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                    keyword_phone_click = str(keyword_phone_tag.get_text())

                #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(',', '')
                    if '<' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace('<', '')
                    if ' ' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(' ', '')

                    #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_click))

            else:
                time.sleep(3)
                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                #검색했던 keyword 정보들을 수집
                tmp_keyword_name_iteration = 0
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    if tmp_keyword_name_iteration == searched_keyword_number:
                        break                
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)
                    tmp_keyword_name_iteration = tmp_keyword_name_iteration + 1

                tmp_keyword_pc_click_iteration = 0
                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    if tmp_keyword_pc_click_iteration == searched_keyword_number:
                        break
                    keyword_pc_click = str(keyword_pc_tag.get_text())
                            
                #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(',', '')
                    if '<' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace('<', '')
                    if ' ' in keyword_pc_click:
                        keyword_pc_click = keyword_pc_click.replace(' ', '')
                            
                #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_click))

                    tmp_keyword_pc_click_iteration = tmp_keyword_pc_click_iteration + 1

                tmp_keyword_phone_click_iteration = 0
                
                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                    if tmp_keyword_phone_click_iteration == searched_keyword_number:
                        break

                    keyword_phone_click = str(keyword_phone_tag.get_text())

                #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(',', '')
                    if '<' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace('<', '')
                    if ' ' in keyword_phone_click:
                        keyword_phone_click = keyword_phone_click.replace(' ', '')

                #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_click))

                    tmp_keyword_phone_click_iteration = tmp_keyword_phone_click_iteration + 1


                ###중간페이지 이동
                normal_start_page = int((a_length-4)/2) + 2

                #중간페이지로 이동
                driver.find_elements_by_class_name('page-item')[normal_start_page].click()
                #그후에 움직이기
                for link_number in range(normal_start_page, normal_start_page + 2):
                    time.sleep(3)
                    
                    #고친부분
                    pageSource = driver.page_source
                    bs = BeautifulSoup(pageSource, 'html.parser')

                    #keyword name 검색결과 저장
                    for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                        keyword_name = keyword_name_tag.get_text()
                        self.keywords_name.append(keyword_name)
                        
                    #키워드 클릭해서 동향 알아보기
                        
                    #고친부분

                    #keyword pc click 검색결과 저장
                    for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                        keyword_pc_click = str(keyword_pc_tag.get_text())
                        
                        #keyword_pc_click 에서 쓸모없는부분 제거
                        if ',' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(',', '')
                        if '<' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace('<', '')
                        if ' ' in keyword_pc_click:
                            keyword_pc_click = keyword_pc_click.replace(' ', '')
                        
                        #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                        self.keywords_pc_search.append(int(keyword_pc_click))

                    
                    #keyword phone click 검색결과 저장
                    for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                        
                        keyword_phone_click = str(keyword_phone_tag.get_text())

                        #keyword_phone_click 에서 쓸모없는부분 제거
                        if ',' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(',', '')
                        if '<' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace('<', '')
                        if ' ' in keyword_phone_click:
                            keyword_phone_click = keyword_phone_click.replace(' ', '')

                        #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                        self.keywords_phone_search.append(int(keyword_phone_click))

                    #다음페이지 click
                    driver.find_elements_by_class_name('page-item')[link_number].click()

        driver.quit()
        return True


    #전체적인값 구하기 But 오류 발생가능성 높음(특히 스마트 스토어)
    #Return 값은 {self.keywords_name, self.keywords_pc_click, self.keywords_phone_click}
    

    def login_naver_ad_total(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        print('[+]Naver Login Starts...')

        baseUrl = 'https://searchad.naver.com/'

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(baseUrl)
        driver.implicitly_wait(5)

        #id, password 입력하기

        driver.find_element_by_xpath('//*[@id="uid"]').send_keys(self.naver_id)
        driver.implicitly_wait(random.randint(2,4))
        driver.find_element_by_xpath('//*[@id="upw"]').send_keys(self.naver_password)
        driver.implicitly_wait(random.randint(2,4))
        ActionChains(driver).send_keys(Keys.RETURN).perform()

        #naver 키워드 도구로 이동
        driver.implicitly_wait(2)

        driver.get('https://manage.searchad.naver.com/front')
        driver.implicitly_wait(random.randint(10, 15))
        try:
            driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()
        except NoSuchElementException as e:
            print(e)
            time.sleep(random.randint(3,5))
            driver.implicitly_wait(2)
            driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/a').click()

        driver.implicitly_wait(random.randint(10, 15))

        try:
            driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        except NoSuchElementException as e:
            print(e)
            time.sleep(random.randint(3,5))
            driver.implicitly_wait(2)
            driver.find_element_by_xpath('//*[@id="navbar-common-header-collapse"]/ul/li[3]/ul/li[3]/a').click()
        

        #keyword 사용자에게 입력받기
        if keyword1 is not None:
            keyword_candidate_one = keyword1
        else:
            keyword_candidate_one = ''

        if keyword2 is not None:
            keyword_candidate_two = keyword2
        else:
            keyword_candidate_two = ''

        if keyword3 is not None:
            keyword_candidate_three = keyword3
        else:
            keyword_candidate_three = ''

        if keyword4 is not None:
            keyword_candidate_four = keyword4
        else:
            keyword_candidate_four = ''
        
        if keyword5 is not None:
            keyword_candidate_five = keyword5
        else:
            keyword_candidate_five = ''

        #keyword 광고 textarea에 입력하기
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_one)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_two)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_three)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_four)
        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(Keys.RETURN)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/div/textarea').send_keys(keyword_candidate_five)

        driver.find_element_by_xpath('/html/body/elena-root/elena-wrap/div/div[2]/elena-tool-wrap/div/div/div/div/elena-keyword-planner/div[2]/div[1]/div[1]/div[3]/button').click()

        driver.implicitly_wait(1)

        try:
            if driver.find_element_by_xpath('//*[@id="toast-container"]/div'):
                print('[-] 금지된 키워드가 존재합니다. 다른 키워드를 입력하여 다시 실행해 주세요!')
                driver.quit()
                return False
        except NoSuchElementException as e:
            time.sleep(3)
            
            #pageSource가지고 오기
            pageSource = driver.page_source
            bs = BeautifulSoup(pageSource, 'html.parser')
            
            #li 총 갯수를 가지고 오기
            the_number_of_link = len(bs.findAll('li', {'class': 'page-item'})) - 4

            for link_number in range(3, the_number_of_link+3):
                time.sleep(3)

                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')

                #keyword name 검색결과 저장
                for keyword_name_tag in bs.findAll('span', {'class': 'common planner'}):
                    keyword_name = keyword_name_tag.get_text()
                    self.keywords_name.append(keyword_name)

                #keyword pc click 검색결과 저장
                for keyword_pc_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyPcQcCnt'}):
                    keyword_pc_search = str(keyword_pc_tag.get_text())
                    
                    #keyword_pc_click 에서 쓸모없는부분 제거
                    if ',' in keyword_pc_search:
                        keyword_pc_search = keyword_pc_search.replace(',', '')
                    if '<' in keyword_pc_search:
                        keyword_pc_search = keyword_pc_search.replace('<', '')
                    if ' ' in keyword_pc_search:
                        keyword_pc_search = keyword_pc_search.replace(' ', '')
                    
                    #keyword_pc_click을 int 형으로 바꾸고 keywords_pc_click 리스트에 저장
                    self.keywords_pc_search.append(int(keyword_pc_search))


                #keyword phone click 검색결과 저장
                for keyword_phone_tag in bs.findAll('td', {'class': 'elenaColumn-monthlyMobileQcCnt'}):
                    
                    keyword_phone_search = str(keyword_phone_tag.get_text())

                    #keyword_phone_click 에서 쓸모없는부분 제거
                    if ',' in keyword_phone_search:
                        keyword_phone_search = keyword_phone_search.replace(',', '')
                    if '<' in keyword_phone_search:
                        keyword_phone_search = keyword_phone_search.replace('<', '')
                    if ' ' in keyword_phone_search:
                        keyword_phone_search = keyword_phone_search.replace(' ', '')

                    #keywords phone click list안에 int형으로 바꾼 keyword phone click 을 삽입한다.
                    self.keywords_phone_search.append(int(keyword_phone_search))
                

                #다음페이지 click
                driver.find_elements_by_class_name('page-item')[link_number].click()
        
        print('[+]Naver Login Ends...')
        return True


    def get_smart_store_products(self):
        print('[+]Smart Store Section Starts...')
        shoppingUrl = 'https://shopping.naver.com'

        #쪼개지 않고 진행
        if len(self.keywords_name) < 2:
            pass
        #1번 쪼개고 진행
        elif len(self.keywords_name) >= 2 and len(self.keywords_name) < 16:
            self.smart_store_products = self.smart_store_products + split_two_list(self.keywords_name, shoppingUrl)
            return True
        #2번 쪼개고 진행
        elif len(self.keywords_name) >= 16 and len(self.keywords_name) < 32:
            #1번 쪼개기
            first_divide_keywords_number = give_me_the_number_divided_two(self.keywords_name)
            tmp_keywords_one = first_keywords_part(first_divide_keywords_number, self.keywords_name)
            tmp_keywords_two = second_keywords_part(first_divide_keywords_number, self.keywords_name)
            #2번 쪼개기
            keywords_part_one = split_two_list(tmp_keywords_one, shoppingUrl)
            keywords_part_two = split_two_list(tmp_keywords_two, shoppingUrl)

            self.smart_store_products = keywords_part_one + keywords_part_two

            return True
        #3번 쪼개고 진행
        elif len(self.keywords_name) >= 32 and len(self.keywords_name) < 64:
            #1번 쪼개기
            first_divide_keywords_number = give_me_the_number_divided_two(self.keywords_name)
            tmp_keywords_one = first_keywords_part(first_divide_keywords_number, self.keywords_name)
            tmp_keywords_two = second_keywords_part(first_divide_keywords_number, self.keywords_name)
            #2번 쪼개기
            #2-1 쪼기개
            second_first_keywords_number = give_me_the_number_divided_two(tmp_keywords_one)
            tmp_tmp_first_one = first_keywords_part(second_first_keywords_number, tmp_keywords_one)
            tmp_tmp_first_two = second_keywords_part(second_first_keywords_number, tmp_keywords_one)

            #2-2 쪼개기
            second_second_keywords_number = give_me_the_number_divided_two(tmp_keywords_two)
            tmp_tmp_second_one = first_keywords_part(second_second_keywords_number, tmp_keywords_two)
            tmp_tmp_second_two = second_keywords_part(second_second_keywords_number, tmp_keywords_two)

            #3번 쪼개기
            keywords_part_one = split_two_list(tmp_tmp_first_one, shoppingUrl)
            keywords_part_two = split_two_list(tmp_tmp_first_two, shoppingUrl)
            keywords_part_three = split_two_list(tmp_tmp_second_one, shoppingUrl)
            keywords_part_four = split_two_list(tmp_tmp_second_two, shoppingUrl)

            self.smart_store_products = keywords_part_one + keywords_part_two + keywords_part_three + keywords_part_four
            
            return True
        #4번 쪼개고 진행
        elif len(self.keywords_name) >= 64 and len(self.keywords_name) < 128:
            #1번 쪼개기
            first_divide_keywords_number = give_me_the_number_divided_two(self.keywords_name)
            tmp_keywords_one = first_keywords_part(first_divide_keywords_number, self.keywords_name)
            tmp_keywords_two = second_keywords_part(first_divide_keywords_number, self.keywords_name)

            #2번 쪼개기
            #2-1 쪼기개
            second_first_keywords_number = give_me_the_number_divided_two(tmp_keywords_one)
            tmp_tmp_first_one = first_keywords_part(second_first_keywords_number, tmp_keywords_one)
            tmp_tmp_first_two = second_keywords_part(second_first_keywords_number, tmp_keywords_one)

            #2-2 쪼개기
            second_second_keywords_number = give_me_the_number_divided_two(tmp_keywords_two)
            tmp_tmp_second_one = first_keywords_part(second_second_keywords_number, tmp_keywords_two)
            tmp_tmp_second_two = second_keywords_part(second_second_keywords_number, tmp_keywords_two)

            #3번 쪼개기
            #3-1-1
            third_first_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_one)
            tmp_tmp_tmp_first_first_one = first_keywords_part(third_first_first_keywords_number, tmp_tmp_first_one)
            tmp_tmp_tmp_first_first_two = second_keywords_part(third_first_first_keywords_number, tmp_tmp_first_one)

            third_first_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_two)
            tmp_tmp_tmp_first_second_one = first_keywords_part(third_first_second_keywords_number, tmp_tmp_first_two)
            tmp_tmp_tmp_first_second_two = second_keywords_part(third_first_second_keywords_number, tmp_tmp_first_two)
            #3-1-2
            third_second_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_one)
            tmp_tmp_tmp_second_first_one = first_keywords_part(third_second_first_keywords_number, tmp_tmp_second_one)
            tmp_tmp_tmp_second_first_two = second_keywords_part(third_second_first_keywords_number, tmp_tmp_second_one)

            third_second_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_two)
            tmp_tmp_tmp_second_second_one = first_keywords_part(third_second_second_keywords_number, tmp_tmp_second_two)
            tmp_tmp_tmp_second_second_two = second_keywords_part(third_second_second_keywords_number, tmp_tmp_second_two)
                
            #4번 쪼개기
            tmp_keywords_one = split_two_list(tmp_tmp_tmp_first_first_one, shoppingUrl)
            tmp_keywords_two = split_two_list(tmp_tmp_tmp_first_first_two, shoppingUrl)
            tmp_keywords_three = split_two_list(tmp_tmp_tmp_first_second_one, shoppingUrl)
            tmp_keywords_four = split_two_list(tmp_tmp_tmp_first_second_two, shoppingUrl)
            tmp_keywords_five = split_two_list(tmp_tmp_tmp_second_first_one, shoppingUrl)
            tmp_keywords_six = split_two_list(tmp_tmp_tmp_second_first_two, shoppingUrl)
            tmp_keywords_seven = split_two_list(tmp_tmp_tmp_second_second_one, shoppingUrl)
            tmp_keywords_eight = split_two_list(tmp_tmp_tmp_second_second_two, shoppingUrl)
            
            result_keywords = tmp_keywords_one + tmp_keywords_two + tmp_keywords_three + tmp_keywords_four + tmp_keywords_five + tmp_keywords_six + tmp_keywords_seven + tmp_keywords_eight
            self.smart_store_products = self.smart_store_products + result_keywords

            return True

        #5번 쪼개고 진행
        else:
            #1번 쪼개기
            first_divide_keywords_number = give_me_the_number_divided_two(self.keywords_name)
            tmp_keywords_one = first_keywords_part(first_divide_keywords_number, self.keywords_name)
            tmp_keywords_two = second_keywords_part(first_divide_keywords_number, self.keywords_name)

            #2번 쪼개기
            #2-1 쪼기개
            second_first_keywords_number = give_me_the_number_divided_two(tmp_keywords_one)
            tmp_tmp_first_one = first_keywords_part(second_first_keywords_number, tmp_keywords_one)
            tmp_tmp_first_two = second_keywords_part(second_first_keywords_number, tmp_keywords_one)

            #2-2 쪼개기
            second_second_keywords_number = give_me_the_number_divided_two(tmp_keywords_two)
            tmp_tmp_second_one = first_keywords_part(second_second_keywords_number, tmp_keywords_two)
            tmp_tmp_second_two = second_keywords_part(second_second_keywords_number, tmp_keywords_two)

            #3번 쪼개기
            #3-1-1
            third_first_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_one)
            tmp_tmp_tmp_first_first_one = first_keywords_part(third_first_first_keywords_number, tmp_tmp_first_one)
            tmp_tmp_tmp_first_first_two = second_keywords_part(third_first_first_keywords_number, tmp_tmp_first_one)

            third_first_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_two)
            tmp_tmp_tmp_first_second_one = first_keywords_part(third_first_second_keywords_number, tmp_tmp_first_two)
            tmp_tmp_tmp_first_second_two = second_keywords_part(third_first_second_keywords_number, tmp_tmp_first_two)
            #3-1-2
            third_second_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_one)
            tmp_tmp_tmp_second_first_one = first_keywords_part(third_second_first_keywords_number, tmp_tmp_second_one)
            tmp_tmp_tmp_second_first_two = second_keywords_part(third_second_first_keywords_number, tmp_tmp_second_one)

            third_second_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_first_two)
            tmp_tmp_tmp_second_second_one = first_keywords_part(third_second_second_keywords_number, tmp_tmp_second_two)
            tmp_tmp_tmp_second_second_two = second_keywords_part(third_second_second_keywords_number, tmp_tmp_second_two)

            #4번 쪼개기
            #4-1-1
            fourth_first_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_first_first_one)
            tmp_tmp_tmp_tmp_first_first_first_one = first_keywords_part(fourth_first_first_keywords_number, tmp_tmp_tmp_first_first_one)
            tmp_tmp_tmp_tmp_first_first_first_two = second_keywords_part(fourth_first_first_keywords_number, tmp_tmp_tmp_first_first_one)

            #4-1-2
            fourth_first_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_first_first_two)
            tmp_tmp_tmp_tmp_first_first_second_one = first_keywords_part(fourth_first_second_keywords_number, tmp_tmp_tmp_first_first_two)
            tmp_tmp_tmp_tmp_first_first_second_two = second_keywords_part(fourth_first_second_keywords_number, tmp_tmp_tmp_first_first_two)

            #4-2-1
            fourth_second_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_first_second_one)
            tmp_tmp_tmp_tmp_second_first_first_one = first_keywords_part(fourth_second_first_keywords_number, tmp_tmp_tmp_first_second_one)
            tmp_tmp_tmp_tmp_second_first_first_two = second_keywords_part(fourth_second_first_keywords_number, tmp_tmp_tmp_first_second_one)
            #4-2-2
            fourth_second_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_first_second_two)
            tmp_tmp_tmp_tmp_second_first_second_one = first_keywords_part(fourth_second_second_keywords_number, tmp_tmp_tmp_first_second_two)
            tmp_tmp_tmp_tmp_second_first_second_two = second_keywords_part(fourth_second_second_keywords_number, tmp_tmp_tmp_first_second_two)

            #4-3-1
            fourth_third_first_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_second_first_one)
            tmp_tmp_tmp_tmp_third_first_first_one = first_keywords_part(fourth_third_first_first_keywords_number, tmp_tmp_tmp_second_first_one)
            tmp_tmp_tmp_tmp_third_first_first_two = second_keywords_part(fourth_third_first_first_keywords_number, tmp_tmp_tmp_second_first_one)

            #4-3-2
            fourth_third_first_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_second_first_two)
            tmp_tmp_tmp_tmp_third_first_second_one = first_keywords_part(fourth_third_first_second_keywords_number, tmp_tmp_tmp_second_first_two)
            tmp_tmp_tmp_tmp_third_first_second_two = second_keywords_part(fourth_third_first_second_keywords_number, tmp_tmp_tmp_second_first_two)

            #4-4-1
            fourth_fourth_second_first_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_second_second_one)
            tmp_tmp_tmp_tmp_fourth_first_first_one = first_keywords_part(fourth_fourth_second_first_keywords_number, tmp_tmp_tmp_second_second_one)
            tmp_tmp_tmp_tmp_fourth_first_first_two = second_keywords_part(fourth_fourth_second_first_keywords_number, tmp_tmp_tmp_second_second_one)
            #4-4-2
            fourth_fourth_second_second_keywords_number = give_me_the_number_divided_two(tmp_tmp_tmp_second_second_two)
            tmp_tmp_tmp_tmp_fourth_first_second_one = first_keywords_part(fourth_fourth_second_second_keywords_number, tmp_tmp_tmp_second_second_two)
            tmp_tmp_tmp_tmp_fourth_first_second_two = second_keywords_part(fourth_fourth_second_second_keywords_number, tmp_tmp_tmp_second_second_two)

            tmp_keywords_one = split_two_list(tmp_tmp_tmp_tmp_first_first_first_one, shoppingUrl)
            tmp_keywords_two = split_two_list(tmp_tmp_tmp_tmp_first_first_first_two, shoppingUrl)
            tmp_keywords_three = split_two_list(tmp_tmp_tmp_tmp_first_first_second_one, shoppingUrl)
            tmp_keywords_four = split_two_list(tmp_tmp_tmp_tmp_first_first_second_two, shoppingUrl)
            tmp_keywords_five = split_two_list(tmp_tmp_tmp_tmp_second_first_first_one, shoppingUrl)
            tmp_keywords_six = split_two_list(tmp_tmp_tmp_tmp_second_first_first_two, shoppingUrl)
            tmp_keywords_seven = split_two_list(tmp_tmp_tmp_tmp_second_first_second_one, shoppingUrl)
            tmp_keywords_eight = split_two_list(tmp_tmp_tmp_tmp_second_first_second_two, shoppingUrl)
            tmp_keywords_nine = split_two_list(tmp_tmp_tmp_tmp_third_first_first_one, shoppingUrl)
            tmp_keywords_ten = split_two_list(tmp_tmp_tmp_tmp_third_first_first_two, shoppingUrl)
            tmp_keywords_eleven = split_two_list(tmp_tmp_tmp_tmp_third_first_second_one, shoppingUrl)
            tmp_keywords_twelve = split_two_list(tmp_tmp_tmp_tmp_third_first_second_two, shoppingUrl)
            tmp_keywords_thirteen = split_two_list(tmp_tmp_tmp_tmp_fourth_first_first_one, shoppingUrl)
            tmp_keywords_fourteen = split_two_list(tmp_tmp_tmp_tmp_fourth_first_first_two, shoppingUrl)
            tmp_keywords_fifteen = split_two_list(tmp_tmp_tmp_tmp_fourth_first_second_one, shoppingUrl)
            tmp_keywords_sixteen = split_two_list(tmp_tmp_tmp_tmp_fourth_first_second_two, shoppingUrl)

            result_keywords = tmp_keywords_one + tmp_keywords_two + tmp_keywords_three + tmp_keywords_four + tmp_keywords_five + tmp_keywords_six + tmp_keywords_seven + tmp_keywords_eight + tmp_keywords_nine + tmp_keywords_ten + tmp_keywords_eleven + tmp_keywords_twelve + tmp_keywords_thirteen + tmp_keywords_fourteen + tmp_keywords_fifteen + tmp_keywords_sixteen

            self.smart_store_products = self.smart_store_products + result_keywords

        return True


    #Cafe Crawling
    def get_the_number_of_cafe_contents(self):
        try:
            print('[+]Cafe Section Starts...')
            cafeUrl = 'https://section.cafe.naver.com'

            options = webdriver.ChromeOptions()
            options.add_argument('headless')

            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            options.add_experimental_option('excludeSwitches', ['enable-automation'])


            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

            for keyword in self.keywords_name:
                driver.get(cafeUrl)
                driver.implicitly_wait(random.randint(10,15))

                mainPageSource = driver.page_source
                bs = BeautifulSoup(mainPageSource, 'html.parser')
                try:
                    #카페 input 창에다가 keyword 삽입
                    driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/form/fieldset/div/div/input').send_keys(keyword)
                except NoSuchElementException as e:
                    #카페 input 창에다가 keyword 삽입
                    driver.find_element_by_name('snb_search_text').send_keys(keyword)

                #엔터버튼 누르기
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                driver.implicitly_wait(random.randint(10, 15))    
                #the_number_of_cafe_contents 와 비교할 string을 가지고 오기
                the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')

                #compare_tmp_number_of_cafe_contents 가 ''일 경우 0일 가능성이 있으므로 10번정도 다시한번 refresh후 확인한다.
                number = 0
                if the_number_of_cafe_contents.text == '':
                    while number < 10:
                        driver.refresh()
                        driver.implicitly_wait(random.randint(10,15))
                        the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')
                        if the_number_of_cafe_contents.text != '':
                            break
                        number = number + 1

                #두번째 검사
                number_two = 0
                if the_number_of_cafe_contents.text == '':
                    while number_two < 15:
                        driver.refresh()
                        driver.implicitly_wait(random.randint(20, 25))
                        the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')
                        if the_number_of_cafe_contents.text != '':
                            break

                        number_two = number_two + 1


                #만약 compare_tmp_number_of_cafe_contents가 ''일경우 0을 cafe_contents에 넣고 진행을 종료(continue 이용 because of for syntax)
                if the_number_of_cafe_contents.text == '':
                    self.cafe_contents.append(0)
                    #다시 for 문으로 올라가 새로운 keyword 대입
                    continue
                else:
                    the_number_of_cafe_contents = the_number_of_cafe_contents.text
                    
                    tmp_number_list_form = []
                    for index in the_number_of_cafe_contents:
                        if index is ',':
                            continue
                        tmp_number_list_form.append(index)

                    the_number_of_cafe_contents = ''.join(tmp_number_list_form)

                    self.cafe_contents.append(int(the_number_of_cafe_contents))
                    
                    print(self.cafe_contents)

            print('[+]Cafe Section Ends...')
            driver.quit()
        except WebDriverException as e:
            print('[-]There Is An Error {}'.format(e))

            driver.quit()
            print('[+]Cafe Section Restarts...')
            cafeUrl = 'https://section.cafe.naver.com'

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            options.add_experimental_option('excludeSwitches', ['enable-automation'])

            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

            for keyword in self.keywords_name:
                driver.get(cafeUrl)
                driver.implicitly_wait(random.randint(10,15))

                mainPageSource = driver.page_source
                bs = BeautifulSoup(mainPageSource, 'html.parser')
                try:
                    #카페 input 창에다가 keyword 삽입
                    driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/form/fieldset/div/div/input').send_keys(keyword)
                except NoSuchElementException as e:
                    #카페 input 창에다가 keyword 삽입
                    driver.find_element_by_name('snb_search_text').send_keys(keyword)

                #엔터버튼 누르기
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                driver.implicitly_wait(random.randint(10, 15))    
                #the_number_of_cafe_contents 와 비교할 string을 가지고 오기
                the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')

                #compare_tmp_number_of_cafe_contents 가 ''일 경우 0일 가능성이 있으므로 10번정도 다시한번 refresh후 확인한다.
                number = 0
                if the_number_of_cafe_contents.text == '':
                    while number < 10:
                        driver.refresh()
                        driver.implicitly_wait(random.randint(10,15))
                        the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')
                        if the_number_of_cafe_contents.text != '':
                            break
                        number = number + 1

                #두번째 검사
                number_two = 0
                if the_number_of_cafe_contents.text == '':
                    while number_two < 15:
                        driver.refresh()
                        driver.implicitly_wait(random.randint(20, 25))
                        the_number_of_cafe_contents = driver.find_element_by_xpath('//*[@id="content_srch"]/div[3]/div/h3/span/em')
                        if the_number_of_cafe_contents.text != '':
                            break

                        number_two = number_two + 1


                #만약 compare_tmp_number_of_cafe_contents가 ''일경우 0을 cafe_contents에 넣고 진행을 종료(continue 이용 because of for syntax)
                if the_number_of_cafe_contents.text == '':
                    self.cafe_contents.append(0)
                    #다시 for 문으로 올라가 새로운 keyword 대입
                    continue
                else:
                    the_number_of_cafe_contents = the_number_of_cafe_contents.text
                    
                    tmp_number_list_form = []
                    for index in the_number_of_cafe_contents:
                        if index is ',':
                            continue
                        tmp_number_list_form.append(index)

                    the_number_of_cafe_contents = ''.join(tmp_number_list_form)

                    self.cafe_contents.append(int(the_number_of_cafe_contents))
                    
                    print(self.cafe_contents)

            print('[+]Cafe Section Ends...')
            driver.quit()

            time.sleep(random.randint(3,5))

    #Blog Crawling
    #Return 값은 blog_contents 리스트
    def get_the_number_of_blog_contents(self):
        try:
            print('[+]Blog Section Starts...')

            blogUrl = 'https://section.blog.naver.com'

            options = webdriver.ChromeOptions()
            options.add_argument('headless')

            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            options.add_experimental_option('excludeSwitches', ['enable-automation'])


            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

            for keyword in self.keywords_name:
                driver.get(blogUrl)
                driver.implicitly_wait(random.randint(10,15))

                mainPageSource = driver.page_source
                bs = BeautifulSoup(mainPageSource, 'html.parser')
                try:
                    #input 창에다가 keyword 삽입
                    driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input').send_keys(keyword)
                except NoSuchElementException as e:
                    #input 창에다가 keyword 삽입
                    driver.find_element_by_name('sectionBlogQuery').send_keys(keyword)

                #엔터버튼 누르기
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                #검색페이지로 이동
                driver.implicitly_wait(random.randint(30,35))

                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')
                #블로그 컨텐츠 수 추출하기
                the_number_of_blog_contents = bs.find('em', {'class': 'search_number'})
                
                if the_number_of_blog_contents is None:
                    while the_number_of_blog_contents is None:
                        #Refresh 해주기
                        driver.refresh()
                        driver.implicitly_wait(random.randint(30,35))

                        pageSource = driver.page_source
                        bs = BeautifulSoup(pageSource, 'html.parser')
                        #다시 블로그 컨텐츠 추출하기
                        the_number_of_blog_contents = bs.find('em', {'class': 'search_number'})
                        
                    
                    the_number_of_blog_contents = the_number_of_blog_contents.get_text()
                    #the_number_of_blog_contents 에서 필요하지 않은 부분 삭제
                    the_number_of_blog_contents = the_number_of_blog_contents.replace('건','')
                    the_number_of_blog_contents = the_number_of_blog_contents.replace(',', '')

                    #int형으로 바꾸고나서 the_number_of_blog_contents를 blog_contents 배열에 저장하기
                    self.blog_contents.append(int(the_number_of_blog_contents))

                    
                else:
                    the_number_of_blog_contents = the_number_of_blog_contents.get_text()
                    the_number_of_blog_contents = the_number_of_blog_contents.replace('건','')
                    the_number_of_blog_contents = the_number_of_blog_contents.replace(',', '')

                    #int형으로 바꾸고나서 the_number_of_blog_contents를 blog_contents 배열에 저장하기
                    self.blog_contents.append(int(the_number_of_blog_contents))
                
                print(self.blog_contents)    
            driver.quit()

            print('[+]Blog Section Ends...')
            
            return True
        except WebDriverException as e:
            print('[-]There Is An Error {}'.format(e))
            driver.quit()

            print('[+]Blog Section Restarts...')

            blogUrl = 'https://section.blog.naver.com'

            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
            options.add_experimental_option('excludeSwitches', ['enable-automation'])

            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

            for keyword in self.keywords_name:
                driver.get(blogUrl)
                driver.implicitly_wait(random.randint(10,15))

                mainPageSource = driver.page_source
                bs = BeautifulSoup(mainPageSource, 'html.parser')
                try:
                    #input 창에다가 keyword 삽입
                    driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input').send_keys(keyword)
                except NoSuchElementException as e:
                    #input 창에다가 keyword 삽입
                    driver.find_element_by_name('sectionBlogQuery').send_keys(keyword)

                #엔터버튼 누르기
                ActionChains(driver).send_keys(Keys.RETURN).perform()

                #검색페이지로 이동
                driver.implicitly_wait(random.randint(30,35))

                pageSource = driver.page_source
                bs = BeautifulSoup(pageSource, 'html.parser')
                #블로그 컨텐츠 수 추출하기
                the_number_of_blog_contents = bs.find('em', {'class': 'search_number'})
                
                if the_number_of_blog_contents is None:
                    while the_number_of_blog_contents is None:
                        #Refresh 해주기
                        driver.refresh()
                        driver.implicitly_wait(random.randint(30,35))

                        pageSource = driver.page_source
                        bs = BeautifulSoup(pageSource, 'html.parser')
                        #다시 블로그 컨텐츠 추출하기
                        the_number_of_blog_contents = bs.find('em', {'class': 'search_number'})
                        
                    
                    the_number_of_blog_contents = the_number_of_blog_contents.get_text()
                    #the_number_of_blog_contents 에서 필요하지 않은 부분 삭제
                    the_number_of_blog_contents = the_number_of_blog_contents.replace('건','')
                    the_number_of_blog_contents = the_number_of_blog_contents.replace(',', '')

                    #int형으로 바꾸고나서 the_number_of_blog_contents를 blog_contents 배열에 저장하기
                    self.blog_contents.append(int(the_number_of_blog_contents))

                    
                else:
                    the_number_of_blog_contents = the_number_of_blog_contents.get_text()
                    the_number_of_blog_contents = the_number_of_blog_contents.replace('건','')
                    the_number_of_blog_contents = the_number_of_blog_contents.replace(',', '')

                    #int형으로 바꾸고나서 the_number_of_blog_contents를 blog_contents 배열에 저장하기
                    self.blog_contents.append(int(the_number_of_blog_contents))
                
                print(self.blog_contents)    
            driver.quit()

            print('[+]Blog Section Ends...')
            
            return True
            

    # JSON 형식 데이터로 만들기
    def make_json_data(self):
        for index in range(0, len(self.keywords_name)):
            keyword = {
                'keyword_name': self.keywords_name[index],
                'keyword_pc_search': self.keywords_pc_search[index],
                'keyword_phone_search': self.keywords_phone_search[index],
                'naver_blog_contents': self.blog_contents[index],
                'naver_cafe_contents': self.cafe_contents[index],
                'smart_store_products': self.smart_store_products[index],
                'naver_blog_contents_divide_keyword_pc_search': self.blog_contents[index] / self.keywords_pc_search[index],
                'naver_blog_contents_divide_keyword_phone_search': self.blog_contents[index] / self.keywords_phone_search[index],
                'naver_blog_contents_divide_all_keyword_search': self.blog_contents[index] / (self.keywords_pc_search[index] + self.keywords_phone_search[index]),
                'naver_cafe_contents_divide_keyword_pc_search': self.cafe_contents[index] / self.keywords_pc_search[index],
                'naver_cafe_contents_divide_keyword_phone_search': self.cafe_contents[index]/ self.keywords_phone_search[index],
                'naver_cafe_contents_divide_all_keyword_search': self.cafe_contents[index] / (self.keywords_pc_search[index] + self.keywords_phone_search[index]),
                'naver_smart_store_divide_keyword_pc_search': self.smart_store_products[index] / self.keywords_pc_search[index],
                'naver_smart_store_divide_keyword_phone_search': self.smart_store_products[index] / self.keywords_phone_search[index],
                'naver_smart_store_divide_all_keyword_search': self.smart_store_products[index] / (self.keywords_pc_search[index] + self.keywords_phone_search[index])
            }
            self.keywords.append(keyword)

        return True

    def total_process(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        check_success = self.login_naver_ad_total(keyword1, keyword2, keyword3, keyword4, keyword5)
        if check_success:
            try:
                self.get_the_number_of_blog_contents()
                self.get_the_number_of_cafe_contents()
                self.get_smart_store_products()
                self.make_json_data()
                return True
            except:
                print('[-]Something Went Wrong! Try It Again...')
                return False
        else:
            print('[-]Login Fail... Try It Again!')
            return False

    def popular_200_process(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        check_success = self.login_naver_ad_200_popular(keyword1, keyword2, keyword3, keyword4, keyword5)
        if check_success:
            try:
                self.get_the_number_of_blog_contents()
                self.get_the_number_of_cafe_contents()
                self.get_smart_store_products()
                self.make_json_data()
                return True
            except:
                print('[-]Something Went Wrong! Try It Again...')
                return False
        else:
            print('[-]Login Fail... Try It Again!')
            return False

    def unpopular_200_process(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        check_success = self.login_naver_ad_200_unpopular(keyword1, keyword2, keyword3, keyword4, keyword5)
        if check_success:
            try:
                self.get_the_number_of_blog_contents()
                self.get_the_number_of_cafe_contents()
                self.get_smart_store_products()
                self.make_json_data()
                return True
            except:
                print('[-]Something Went Wrong! Try It Again...')
                return False
        else:
            print('[-]Login Fail... Try It Again!')
            return False
        

    def normal_200_process(self, keyword1, keyword2, keyword3, keyword4, keyword5):
        check_success = self.login_naver_ad_200_normal(keyword1, keyword2, keyword3, keyword4, keyword5)
        if check_success:
            try:
                self.get_the_number_of_blog_contents()
                self.get_the_number_of_cafe_contents()
                self.get_smart_store_products()
                self.make_json_data()
                return True
            except:
                print('[-]Something Went Wrong! Try It Again...')
                return False
        else:
            print('[-]Login Fail... Try It Again!')
            return False


    #csv file로 파일 저장하기
    def csv_file_store(self, file_name):
        #이름저장하기
        csvFile = open('{}.csv'.format(file_name), 'w+', newline='')
        try:
            writer = csv.writer(csvFile)
            writer.writerow(('keyword_name','keyword_pc_search', 'keyword_phone_search', 'cafe_contents', 'blog_contents', 'smart_store_products', 'naver_blog_contents_divide_keyword_pc_search', 'naver_blog_contents_divide_keyword_phone_search', 'naver_blog_contents_divide_all_keyword_search', 'naver_cafe_contents_divide_keyword_pc_search', 'naver_cafe_contents_divide_keyword_phone_search', 'naver_cafe_contents_divide_all_keyword_search', 'naver_smart_store_divide_keyword_pc_search', 'naver_smart_store_divide_keyword_phone_search', 'naver_smart_store_divide_all_keyword_search'))
            for keyword in self.keywords:
                writer.writerow((keyword['keyword_name'], keyword['keyword_pc_search'], keyword['keyword_phone_search'], keyword['naver_cafe_contents'], keyword['naver_blog_contents'], keyword['smart_store_products'] ,keyword['naver_blog_contents_divide_keyword_pc_search'], keyword['naver_blog_contents_divide_keyword_phone_search'], keyword['naver_blog_contents_divide_all_keyword_search'], keyword['naver_cafe_contents_divide_keyword_pc_search'],keyword['naver_cafe_contents_divide_keyword_phone_search'], keyword['naver_cafe_contents_divide_all_keyword_search'], keyword['naver_smart_store_divide_keyword_pc_search'], keyword['naver_smart_store_divide_keyword_phone_search'], keyword['naver_smart_store_divide_all_keyword_search']))
        except:
            print('[-]Sorry Download Is Fail...')
            return False
        else:
            csvFile.close()
            print('[+] Downloading CSV File  is Complete...')
            return True