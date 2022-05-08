import time
from selenium import webdriver
import pymongo
import configparser

config = configparser.ConfigParser()
config.read('secret_data.ini')

def Crawling(name_list):
    url = 'C:/Users/KDOY/PycharmProjects/chromedriver_win32/chromedriver.exe'
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(url, options=options)

    driver.get("https://www.instagram.com/")
    time.sleep(0.5)
    driver.find_element_by_name('username').send_keys(config['SECRET']['ID'])
    time.sleep(0.5)
    driver.find_element_by_name('password').send_keys(config['SECRET']['PW'])
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
    time.sleep(5)

    Tags = []
    for name in name_list:
        try:
            T = []
            url = "https://www.instagram.com/explore/tags/{}/".format(name)
            driver.get(url)
            time.sleep(10)
            driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a').click()
            time.sleep(5)
            print(name)
            for i in range(9):
                print(i)
                user_ids = driver.find_elements_by_class_name("ZIAjV")
                count = -1
                for user_id in user_ids:
                    if user_id.text == user_ids[1].text and count > 0:
                        more_comment = '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[' + str(
                            count) + ']/li/ul/li/div/button'

                        try:
                            driver.find_element_by_xpath(more_comment).click()
                            time.sleep(5)
                        except:
                            pass
                        break
                    count += 1
                #Tag가 없을 때
                try:
                    tags = driver.find_elements_by_class_name('xil3i')
                    for tag in tags:
                        print(tag.text)
                        T.append(tag.text)
                except:
                    pass

                if i == 8:
                    break
                elif i == 0:
                    driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/button').click()
                    time.sleep(2)
                else:
                    driver.find_element_by_xpath('/html/body/div[6]/div[2]/div/div[2]/button').click()
                    time.sleep(2)

            Deduplication_T = list(set(T))
            Tags.append(Deduplication_T)

        except:
            continue

    return Tags

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Test']
mycol = mydb['Cheonan']

name_list = []
#다이닝코드에서 받아온 천안 음식점 목록
for cate in mycol.find({}, {"_id": 0,"Name": 1, "Score": 1}):
    if cate['Score'] != "":
        name_list.append(cate['Name'])

Tags = Crawling(name_list)