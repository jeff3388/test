#!pip install nest_asyncio
#!pip install twint

from bs4 import BeautifulSoup
from pyppeteer import launch
import asyncio

loop = asyncio.get_event_loop() # 需先宣告好

async def main():
    width, height = 1080,700

    # launch 建立一個新的 browser 物件
    browser = await launch({'headless': False, # True → 打開無頭模式
                            'autoClose': False, # 瀏覽器不會自動關閉
                            'handleSIGINT': False, # 在ctrl+c上關閉瀏覽器進程。默認為 "真"
                            'handleSIGTERM': False,  # 關閉sigterm上的瀏覽器進程。默認值 "真"
                            'handleSIGHUP': False,  # 關閉瀏覽器進程。默認為 "真"
                           
                            'args': ['--disable-infobars', # 取消 'Chrome當前正在受自動化測試軟體控制' 警告
                                     '--window-size='+ str(width) + ',' + str(height) , # 調整視窗大小 
                                     '--start-maximized',  # 調整 browser 為最大化
                                     ]
                           })

    page = await browser.newPage() # 開啟新分頁
    await page.setViewport(viewport={'width': width, 'height': height})
    await page.goto('https://www.scbeasy.com/v1.4/site/presignon/index_en.asp',timeout=6000)
    
    # 登入
    await page.type('#LOGIN', "scbsupanya")
    await page.type('#LogIn > table > tbody > tr:nth-child(3) > td > label > input', "Okay111**")
    
    await page.waitForXPath('//*[@id="lgin"]', timeout=15000) # check login the element is appear
    await asyncio.sleep(3)
    await page.click('#lgin')
    await page.waitForXPath('//*[@id="Img3"]', timeout=15000) # check the buttum is appear that into transfer web page
    await asyncio.sleep(5)
    await page.click('#Img3')
    
    # 確認進入頁面再存 cookies
    await page.waitForXPath('//*[@id="DataProcess_Header_Image"]', timeout=15000)
    
    await asyncio.sleep(5)
    # into transfer flow
    await page.click('#ctl15_AnotherBankAccount_LinkButton') # click Another Bank Account buttum
    await page.waitForXPath('//*[@id="DataProcess_lbtnNoProfile"]', timeout=15000) # wait "Click here for other account" string
    await asyncio.sleep(5)
    await page.click('#DataProcess_lbtnNoProfile')
    await asyncio.sleep(5)
    
    # typing tansfer bank information
    await page.waitForXPath('//*[@id="DataProcess_lbtnViewAccBal"]', timeout=15000)
    await page.evaluate("() => { document.querySelector('#DataProcess_ddlCustBank').selectedIndex=1 }")
    await page.type('#DataProcess_txtCustReceiveAccount', "2240371738")
    await page.type('#DataProcess_txtCustAmount', "20")
    
    await page.waitForXPath('//*[@id="nxt"]', timeout=15000) # check the sumbit buttum is appear
    await page.click('#nxt') # into receive verify code web page


# 可供外部調用執行
def main_function():
    loop.run_until_complete(main())

main_function()