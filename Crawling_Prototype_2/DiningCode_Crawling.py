import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
#변수,리스트 전역변수로 빼주고 메소드화시키기 ~ 5.14


def check_exist(CSS):
    try:
        driver.find_element(By.CSS_SELECTOR,CSS)
    except NoSuchElementException:
        return False
    return True


category = ['밥집']
#category = ['밥집', '술집', '카페']
#city=[]
cccnt=1
for ctgr in category:
    city = ['천안시', '아산시', '당진시', '계룡시', '공주시', '금산군', '논산시', '보령시', '부여군', '서산시', '서천군', '예산군', '청양군', '태안군', '홍성군']
    url = 'https://www.diningcode.com/list?addr=충남%20천안시&keyword=' + ctgr

    Chrome_url = 'C:/Users/82108/Desktop/yoonho/Individual_Project/crolling/chromedriver.exe'
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(Chrome_url)

    driver.get(url)
    time.sleep(1.5)

    # 20개 더보기 클릭 4번 -> 100개의 음식점 리스트
    for i in range(4):
        driver.find_element(By.XPATH,'//*[@id="map"]/button[2]').click()
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    Block_IDs = []
    Titles = []
    Address=[]
    Scores = []
    Menus = []
    Images = []
    Tel=[]

    # 점수 추출
    score_list = soup.find_all('p', 'Score')
    for scores in score_list:
        num = scores.find_all('span')
        for i in num:
            Scores.append(i.text)

    # 이미지 추출(1개)
    image = soup.find_all('img', 'title')
    for i in image:
        image_src = i.get("src")
        Images.append(image_src)


    # block id 추출
    block = soup.find_all('li', 'PoiBlock')
    for i in block:
        block_id = i.get("id")
        Block_IDs.append(block_id[5:])

    #상세정보 페이지에서 추출
    try:
        for Block_ID in Block_IDs:
            second_url = 'https://www.diningcode.com/profile.php?rid='+Block_ID
            time.sleep(0.5)
            driver.get(second_url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            time.sleep(1.5)

            #제목 추출
            divs = soup.find('div','tit-point')
            title = divs.find('p', 'tit')
            title = title.text

            # 띄어쓰기&공백 제거
            t = []
            tit = ""
            t.append(title.split(" "))
            for i in t[0]:
                tit = tit + i
            Titles.append(tit)

            #메뉴 추출
            M = []
            Price = []
            menus = soup.find_all('p', 'l-txt Restaurant_MenuItem')
            prices = soup.find_all('p', 'r-txt Restaurant_MenuPrice')
            for menu in menus:
                M.append(menu.text[:-1])
            for price in prices:
                Price.append(price.text)
            for i in range(len(M)):
                M[i] += " - " + Price[i]
            Menus.append(M)
    except WebDriverException as e:
        print('에러 발생 에러 내용 : '+e)
        #이미지 여러장(필요시 구현)

        #번호 추출 번호 주소 다없는것도있음

    for name in Titles:
        URL_for_get_address='https://www.google.com/search?q='+'천안시 '+name
        driver.get(URL_for_get_address)
        time.sleep(2)
        try:
            address=driver.find_element(By.CSS_SELECTOR,'#kp-wp-tab-overview > div.TzHB6b.cLjAic.LMRCfc > div > div > div > div > div > div:nth-child(5) > div > div > div > span.LrzXr')
            tel=driver.find_element(By.CSS_SELECTOR,'#kp-wp-tab-overview > div.TzHB6b.cLjAic.LMRCfc > div > div > div > div > div > div:nth-child(8) > div > div > div > span:nth-child(2) > span > a > span > span')
        except NoSuchElementException as e:
            print('Error Occured! Error is : '+e)
            try:
                driver.get('https://www.google.com/maps/search/천안시 '+name)
                time.sleep(5)
                driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[3]').click()
                time.sleep(5)
                address = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[1]/button/div[1]/div[2]/div[1]')
                tel = driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[3]/button/div[1]/div[2]/div[1]')
            except Exception as e:
                print('에러 발생 무슨 에러냐?  >> '+e)
        print(name+' 의 주소: '+address.text+'\n전번 :'+tel.text)
        Tel.append(tel.text)
        Address.append(address.text)
"""    
    for name in Titles:
        URL_for_get_address='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='+'천안시 '+ name
        driver.get(URL_for_get_address)
        time.sleep(2)
        if (check_exist(
                '#place_main_ct > div > section:nth-child(1) > div > div.ct_box_area > div.bizinfo_area > div > div:nth-child(2) > div > ul > li:nth-child(1) > span > a > span.txt')):
            address = driver.find_element(By.CSS_SELECTOR,
                                          '#place_main_ct > div > section:nth-child(1) > div > div.ct_box_area > div.bizinfo_area > div > div:nth-child(2) > div > ul > li:nth-child(1) > span > a > span.txt')
            telnum = driver.find_element(By.CSS_SELECTOR,
                                         '#place_main_ct > div > section > div > div.ct_box_area > div.bizinfo_area > div > div:nth-child(1) > div')
        else:
            telnum = driver.find_element(By.CSS_SELECTOR,
                                         '#loc-main-section-root > section > div > ul > li:nth-child(1) > div._3ZU00._1rBq3 > div._1oH7-._1lPUe')
            driver.find_element(By.CSS_SELECTOR,
                                '#loc-main-section-root > section > div > ul > li:nth-child(1) > div._3ZU00._1rBq3 > div._1B9G6 > div > span > a > span._3nlmL > svg').click()
            time.sleep(1.5)
            address = driver.find_element(By.CSS_SELECTOR,
                                          '#loc-main-section-root > section > div > ul > li:nth-child(1) > div._3ZU00._1rBq3 > div._1B9G6 > div > div > div:nth-child(1)')
        Tel.append(telnum.text)
        Address.append(address.text[3:-2])

"""


"""#####################################################################
    # DB 저장
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['Test']
    mycol = mydb['Info']

    for i in range(len(Titles)):
        # 제목이 DB에 있을 경우
        if mycol.find_one({'Name': Titles[i]}):
            myquery = {"Name": Titles[i]}
            Category_values = {"$set": {"Category": ctgr}}
            Menu_values = {"$set": {"Menu": Menus[i]}}
            Image_values = {"$set": {"Image": Images[i]}}
            Score_values = {"$set": {"Score": Scores[i]}}
            Address_values = {"$set": {"Address": Address[i]}}
            tel_values = {"$set": {"Tell_number": Tel[i]}}
            count = 1
            # 카테고리에 데이터가 이미 있는 경우
            for c in mycol.find({'Name': Titles[i]}, {"_id": 0, "Category": 1}):
                if c['Category'] != "":
                    # print(mycol.find({'Name': Titles[i]}))
                    data = []
                    data.append(c['Category'])
                    data.append(ctgr)
                    mycol.update_one(myquery, {"$set": {"Category": data}})
                else:
                    mycol.update_one(myquery, Category_values)
                count += 1

            mycol.update_one(myquery, Menu_values)
            mycol.update_one(myquery, Image_values)
            mycol.update_one(myquery, Score_values)
            mycol.update_one(myquery, Address_values)

        # 제목이 DB에 없을 경우
        else:
            insert_data = {
                'State': "충청남도",
                'City': "천안시",
                'Address': Address[i],
                'Name': Titles[i],
                'Category': ctgr,
                'Menu': Menus[i],
                'Image': Images[i],
                'Tell_number': Tel[i],
                'Tag': "",
                'Score': Scores[i],
            }

            mycol.insert_one(insert_data)"""