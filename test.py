# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import information
import requests
import datetime  
import random
import time
import csv
import re

import urllib.parse
import json

def client_information(url):
    html = requests.get(url=url,timeout=10).content
    soup = BeautifulSoup(html, "html.parser")

    key_text = []
    key_link = []

    for i in soup:
        i = str(i)
        if i not in ["<br/>"]:
            i = i.split(":")
            key_text += [i[0]]
            key_link += [i[1]]

    return key_link,key_text  # 回傳客戶比對連結、優化關鍵字

def save_csv(file_name, client_link, keyword, empty, pages, rank):
    datetime_dt = datetime.datetime.today() # 獲得當地時間  
    date = datetime_dt.strftime("%Y-%m-%d") # 日期

    with open(file_name , 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([client_link, keyword, empty, pages, rank, date])

def page_rank(pageRank_class,keyword,client_link):
    ### 當前頁面所有連結排序 ###
    pageRank_ls = [v.text for v in pageRank_class]

    ### 抓出關鍵字連結 ###
    key_link = ["".join(re.findall(".*"+ client_link,p)) for p in pageRank_ls if p != []]
    key_link = [i for i in key_link if i != ""]
    
    ### 索引關鍵字排名 ###
    index_rank = [p.find(client_link) for p in pageRank_ls]
    rank = 0
    
    # 若同一個網頁出現兩組關鍵字
    if len(key_link) >= 1:
         for k in index_rank:
                rank += 1
                if k != -1:
                    signal = "抓到關鍵字"
                    return signal,keyword,rank
                          
    
    else:
        signal = "沒抓到關鍵字"
        rank = 0
        return signal,keyword,rank
    
    
def main(search_engine,url,file_name):
    key_link,key_text = client_information(url)
    for client_link, keyword in zip(key_link, key_text):
        
        # 隨機變換UserAgent
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
        url = search_engine + 'search?fr=yfp-search-sb-bucket-836494&p=' + keyword                                            
        res = requests.Session()
        html = res.get(url=url,headers=headers).content
        soup = BeautifulSoup(html, 'html.parser')
        pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
        next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素

        ### 當前頁面所有連結排序 ###
        pageRank_ls = [v.text for v in pageRank_class]

        ### 抓出關鍵字連結 ###
        key_link = ["".join(re.findall(".*"+ client_link,p)) for p in pageRank_ls if p != []]
        key_link = [i for i in key_link if i != ""]

        ### 索引關鍵字排名 ###
        index_rank = [p.find(client_link) for p in pageRank_ls]
        rank = 0

        # 若同一個網頁出現兩組關鍵字
        if len(key_link) >= 1:
            for k in index_rank:
                rank += 1
                if k != -1:
                    print("關鍵字: "+ keyword +" 第 1 頁"+", 第" + str(rank) + "名")

                    random_time = random.randint(5,7)
                    time.sleep(random_time)
                    ######## 存成 CSV 檔案 ########
                    pages = '1'
                    empty = '1'
                    save_csv(file_name, client_link, keyword, empty, pages, rank)

        else:
            random_time = random.randint(5,7)
            time.sleep(random_time)
            url = next_page_class[0].get('href')
            html = res.get(url=url,headers=headers)
            html = html.content
            soup = BeautifulSoup(html, 'html.parser')
            pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
            next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
            signal,keyword,rank = page_rank(pageRank_class,keyword,client_link)
            

            if signal == "抓到關鍵字":
                print("關鍵字: "+ keyword +" 第 2 頁"+", 第" + str(rank) + "名")
                random_time = random.randint(5,7)
                time.sleep(random_time)
                
                ######## 存成 CSV 檔案 ########
                pages = '2'
                empty = '1'
                save_csv(file_name, client_link, keyword, empty, pages, rank)
                
            elif signal == "沒抓到關鍵字":
                random_time = random.randint(5,7)
                time.sleep(random_time)
                url = next_page_class[0].get('href')
                html = res.get(url=url,headers=headers)
                html = html.content
                soup = BeautifulSoup(html, 'html.parser')
                pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
                next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
                signal,keyword,rank = page_rank(pageRank_class,keyword,client_link)

                if signal == "抓到關鍵字":
                    print("關鍵字: "+ keyword +" 第 3 頁"+", 第" + str(rank) + "名")
                    random_time = random.randint(5,7)
                    time.sleep(random_time)

                    ######## 存成 CSV 檔案 ########
                    pages = '3'
                    empty = '1'
                    save_csv(file_name, client_link, keyword, empty, pages, rank)
                
                elif signal == "沒抓到關鍵字":
                    random_time = random.randint(5,7)
                    time.sleep(random_time)

                    url = next_page_class[0].get('href')
                    html = res.get(url=url,headers=headers)
                    html = html.content
                    soup = BeautifulSoup(html, 'html.parser')
                    pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
                    next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
                    signal,keyword,rank = page_rank(pageRank_class,keyword,client_link)
                    

                    if signal == "抓到關鍵字":
                        print("關鍵字: "+ keyword +" 第 4 頁"+", 第" + str(rank) + "名")
                        random_time = random.randint(5,7)
                        time.sleep(random_time)
                        ######## 存成 CSV 檔案 ########
                        pages = '4'
                        empty = '1'
                        save_csv(file_name, client_link, keyword, empty, pages, rank)

                    elif signal == "沒抓到關鍵字":

                        url = next_page_class[0].get('href')
                        html = res.get(url=url,headers=headers)
                        html = html.content
                        soup = BeautifulSoup(html, 'html.parser')
                        pageRank_class = soup.find_all(attrs={"class": "aUrl fz-ms fw-m fc-12th wr-bw lh-17 d-ib tc va-top"}) # 網頁排名元素
                        next_page_class = soup.find_all(attrs={"class": "next"}) # 網頁排名元素
                        signal,keyword,rank = page_rank(pageRank_class,keyword,client_link)

                        random_time = random.randint(5,7)
                        time.sleep(random_time)
                        

                        if signal == "抓到關鍵字":
                            
                            print("關鍵字: "+ keyword +" 第 5 頁"+", 第" + str(rank) + "名")
                            random_time = random.randint(5,7)
                            time.sleep(random_time)
                            ######## 存成 CSV 檔案 ########
                            pages = '5'
                            empty = '1'
                            save_csv(file_name, client_link, keyword, empty, pages, rank)
                            

                        elif signal == "沒抓到關鍵字":
                            print("關鍵字: "+ keyword + "不再前5頁")
                            random_time = random.randint(5,7)
                            time.sleep(random_time)
                            pages = '0'
                            empty = '1'
                            save_csv(file_name, client_link, keyword, empty, pages, rank)

                            random_time = random.randint(5,7)
                            time.sleep(random_time)

url= 'http://superkp.wisenet.tw/txt_yahoo.php'

search_engine = 'https://tw.search.yahoo.com/'

file_name = 'yahoo_rank.csv'
main(search_engine,url,file_name)
