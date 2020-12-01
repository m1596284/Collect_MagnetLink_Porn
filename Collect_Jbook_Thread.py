# -*- coding: UTF-8 -*-
import os
import time
import threading
import requests
import re
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
pyPath, filename = os.path.split(__file__)
chrome_options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 
                            'plugins': 2, 'popups': 2, 'geolocation': 2, 
                            'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                            'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                            'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                            'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                            'durable_storage': 2,'permissions.default.stylesheet':2}}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('blink-settings=imagesEnabled=false') 
chrome_options.add_argument('--headless') 
rpTimeList = []
for simCnt in range(1,3):
    for rpCnt in range(1):
        tStart = time.time()
        main_page = "https://jmvbt.com/serchinfo_censored/topicsbt/topicsbt_2.htm"
        r=requests.get(main_page)
        if r.status_code == requests.codes.ok:
            print("Main_OK")
            soup = BeautifulSoup(r.text, 'html.parser')
            urlMainPage = soup.find_all('a',href=re.compile("content_censored"))
            urlList=[]
            for url in urlMainPage:
                urlList.append(url.get('href'))
        urlList = np.array(urlList)
        urlList = urlList[::2]
        f = open(pyPath + "/Magnet_List.txt","a")
        f.close
        lock = threading.Lock()
        FinalMagnetList = []
        wNum = 42
    # 子執行緒的工作函數
        def job(urll,ii,tNum):
            listCnt = 0
            searchTimes = int(np.ceil(wNum/tNum))
            for listCnt in range(searchTimes):
                try:
                    sub_page = urlList[ii*searchTimes+listCnt]
                except:
                    pass
                driver = webdriver.Chrome(executable_path=pyPath + '/driver/chromedriver.exe',chrome_options=chrome_options)
                driver.get(sub_page)
                driver.find_element_by_tag_name('a').get_attribute('innerHTML')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                urlSubPage = soup.find_all('div', class_='dht_dl_size_content')
                cnt=-1
                for i, url in enumerate(urlSubPage):
                    # print(urlSubPage[i])
                    sizeGB = float(url.get_text("div")[:2])
                    # print(sizeGB)
                    MBGB = url.get_text("div")[-2]
                    if MBGB == "G":
                        if sizeGB > 3:
                            break
                        else:
                            cnt=cnt+1
                    else:
                        cnt=cnt+1
                # print(i)
                # print(cnt)
                if i == cnt :
                    pass
                else:
                    urlManget = soup.find_all('a',href=re.compile("magnet"))
                    urlMagnetList=[]
                    a = urlManget[0]
                    # print(a)
                    # print("99")
                    for url in urlManget:
                        urlMagnetList.append(url.get('href'))
                    urlMagnetList = np.array(urlMagnetList)
                    FinalMagnetList.append(urlMagnetList[i])
                    print(FinalMagnetList)
                    driver.close()

        # 建立 n 個子執行緒
        threads = []
        tNum = simCnt+1
        for ii in range(tNum):
            threads.append(threading.Thread(target = job, args = (urlList,ii,tNum)))
            threads[ii].start()

        # 主執行緒繼續執行自己的工作
        # ...

        # 等待所有子執行緒結束
        for ii in range(tNum):
            threads[ii].join()
        f = open(pyPath + "/Magnet_List.txt","a")
        for x, strr in enumerate(FinalMagnetList):
            f.write(strr)
            f.write("\n")
        f.close 
        tEnd = time.time()
        # print(tEnd-tStart)
        rpTimeList.append(str(simCnt+1))
        rpTimeList.append(str(tEnd-tStart))
        # print("Repeat Done.")

f = open(pyPath + "/Magnet_Timer.txt","w")
for x, strr in enumerate(rpTimeList,start=1):
    if x%2 == 1 :
        f.write(strr + "\t")
    else:
        f.write(strr + "\n")
f.close 
# print("All Done")