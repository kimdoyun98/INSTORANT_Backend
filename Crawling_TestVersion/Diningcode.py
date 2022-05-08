import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo

category = ['밥집', '술집', '카페']

for ctgr in category:
    city = ['천안시', '아산시', '당진시', '계룡시', '공주시', '금산군', '논산시', '보령시', '부여군', '서산시', '서천군', '예산군', '청양군', '태안군', '홍성군']
    url = 'https://www.diningcode.com/list?addr=충남%20천안시&keyword=' + ctgr

    Chrome_url = 'C:/Users/KDOY/PycharmProjects/chromedriver_win32/chromedriver.exe'
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome(Chrome_url, options=options)

    driver.get(url)
    time.sleep(0.5)

    # 20개 더보기 클릭 4번 -> 100개의 음식점 리스트
    for i in range(4):
        driver.find_element_by_xpath('//*[@id="map"]/button[2]').click()
        time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    Block_IDs = []
    Titles = []
    Scores = []
    Menus = []
    Images = []

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
    for Block_ID in Block_IDs:
        second_url = 'https://www.diningcode.com/profile.php?rid='+Block_ID
        driver.get(second_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        time.sleep(0.5)

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

        #이미지 여러장(필요시 구현)


#####################################################################
    # DB 저장
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['Test']
    mycol = mydb['Cheonan']

    for i in range(len(Titles)):
        # 제목이 DB에 있을 경우
        if mycol.find_one({'Name': Titles[i]}):
            myquery = {"Name": Titles[i]}
            Category_values = {"$set": {"Category": ctgr}}
            Menu_values = {"$set": {"Menu": Menus[i]}}
            Image_values = {"$set": {"Image": Images[i]}}
            Score_values = {"$set": {"Score": Scores[i]}}
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

        # 제목이 DB에 없을 경우
        else:
            insert_data = {
                'State': "충청남도",
                'City': "천안시",
                'Address': "",
                'Street_address': "",
                'Name': Titles[i],
                'Category': ctgr,
                'Menu': Menus[i],
                'Image': Images[i],
                'X': "",
                'Y': "",
                'Tell_number': "",
                'Tag': "",
                'Score': Scores[i],
            }

            mycol.insert_one(insert_data)