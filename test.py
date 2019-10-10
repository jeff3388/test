import requests
import re
import time
from bs4 import BeautifulSoup

headers = {
            'Host': 'tw.search.yahoo.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://tw.yahoo.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
                }

search_engine = 'https://tw.search.yahoo.com/'
keyword = 'python 教學'
url = search_engine + 'search?fr=yfp-search-sb-bucket-836494&p=' + keyword                                            
res = requests.Session()
html = res.get(url=url,headers=headers)
html = html.content
soup = BeautifulSoup(html, 'html.parser')
pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
### 當前頁面所有連結排序 ###
pageRank_ls = [v.text for v in pageRank_class]

### 抓出關鍵字連結 ###
key_link = ["".join(re.findall(".*"+ 'pala.tw',p)) for p in pageRank_ls if m != []]
key_link = [i for i in key_link if i != ""]

### 索引關鍵字排名 ###
index_rank = [p.find('pala.tw') for p in pageRank_ls]
rank = 0

# 若同一個網頁出現兩組關鍵字
if len(key_link) >= 1:
    for k in index_rank:
        rank += 1
        if k != -1:
            print("關鍵字: "+ keyword +" 第 1 頁"+", 第" + str(rank) + "名")
    
else:
    time.sleep(5)
    url = next_page_class[0].get('href')
    html = res.get(url=url,headers=headers).content
    soup = BeautifulSoup(html, 'html.parser')
    pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
    next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
    print("page 2")
