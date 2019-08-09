from bs4 import BeautifulSoup
import datetime
import requests
import random
import time
import uuid
import re

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

datetime_dt = datetime.datetime.today()
datetime_str = datetime_dt.strftime("%Y-%m-%d %H:%M:%S") # today date transfer to sting format

t = random.randint(1,100)
time.sleep(t)

# post api
url = 'http://temp.check-article.cfd888.info/test_csv'

contents = get_mac_address()
data = {'test': contents + "--" + datetime_str}

r = requests.post(url=url, data=data, timeout=5)
print(r.text)