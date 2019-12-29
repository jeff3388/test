#!pip install nest_asyncio
#!pip install twint
from pyppeteer import launch
from xvfbwrapper import Xvfb
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
    
    # 改變視窗大小
    await page.setViewport(viewport={'width': width, 'height': height})
    await page.goto('https://www.google.com/',timeout=3000)


# 可供外部調用執行
def main_function():
    loop.run_until_complete(main())


vdisplay = Xvfb()
vdisplay.start()

main_function()

vdisplay.stop()