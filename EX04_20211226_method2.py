##################################################
# Date:　2021.12.26                              #
# Number： 19                                    #
# Name: Tzu-Chun Hsu                             #
##################################################

# Structure:
# Step 1: 先測試一個的情況，觀察規律
# Step 2: 套用到多個的情況

# Problem:
# 1) bs4 select class有空格會不認得，會認為是兩個標籤
# 2) 換頁的問題，不過這題是get相對於post較容易
# 3) 只要書名的主標題 但有的主標題只有 "Python" 需要另外處理

import time
import re
import requests
from bs4 import BeautifulSoup

def getPageContent(soup):
    content = ""
    for data in soup.select("div.book-data-inner.h-full.flex.flex-col.justify-evenly"):
        # book name
        book_tmp = data.select_one("a").text.strip()
        book = re.split(r'[\|\(,｜：-]', book_tmp)[0]
        if book == "Python":
            book = book_tmp
        # publish date
        publish_date = data.select_one("span.publish-date").text.strip()
        # price
        price = data.select_one("span.price").text.strip()

        print(f"{price}\t{publish_date}\t{book}\t")

    return content

url = "https://www.tenlong.com.tw/search?availability=buyable&display=list&keyword=python&langs%5B%5D=all"

# 加上user-agent，來偽裝成一般使用者
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}
# 網站起始url
urlStart = "https://www.tenlong.com.tw/search?availability=buyable&display=list&keyword=python&langs%5B%5D=all"


def python_book_search():
    page = input("請問要顯示幾頁?")

    try:
        for i in range(1, int(page) + 1):
            print("=" * 10, "Page", i, "START", "=" * 10)

            response = requests.get(url, headers=headers)

            content = getPageContent(soup)
            # 顯示結果網頁內容
            # print(response.text)
            # 建立BeautifulSoup物件
            soup = BeautifulSoup(response.text, "html.parser")

            print("=" * 10, "Page", i, "END", "=" * 10)
            time.sleep(5)

            # 取得上頁連結
            link = soup.select("div.btn-group.btn-group-paging a")
            url = urlStart + link[1]["href"]

    except ValueError:
        print("輸入錯誤，請輸入正整數")


python_book_search()


# Optimization
# 1) 頁數超過上限 如何知道?
# 2) 未來數據量很大，相較time.sleep() 可以做分散式爬蟲節省時間
# 3) 未來數據量很大，應該把數據回傳到SQL



