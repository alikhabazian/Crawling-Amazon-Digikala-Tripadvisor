import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from IPython.display import clear_output
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from IPython.display import clear_output
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


def list_str(lis):
    q=[]
    for i in range(len(lis)):
        q.append(lis[i].text.strip())
    return q



def trip_adviser_do(link,max_page):
#     link='https://www.tripadvisor.com/Attraction_Review-g295423-d8123033-Reviews-Chahar_Bagh_Theological_School-Isfahan_Isfahan_Province.html'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)

    details=[]
    levels=[]
    dates=[]
    idess=[]
    likess=[]
    titles=[]
    mesages=[]
    first=1
    
    
    content = driver.page_source
    soup = BeautifulSoup(content)

    name=soup.find(attrs={"class":"DrjyGw-P _1SRa-qNz qf3QTY0F"}).text
    


    count=1
    while(max_page>=count):
        comments_bad = driver.find_elements_by_xpath('//div[@class="_3MTo5es_"]')+driver.find_elements_by_xpath('//div[@class="_2icGD8ND ZF3Q2Ihz _1yHOEhrb"]')
        
        for i in range(len(comments_bad)):
            driver.execute_script("""
               var l = document.getElementsByClassName("_3MTo5es_")[0];
               l.parentNode.removeChild(l);
            """)
        count=count+1
        time.sleep(5)
        positive_list = driver.find_elements_by_xpath('//a[contains(@href,"/Profile/")]')
        positive2_list = driver.find_elements_by_xpath('//a[contains(@target,"_self")]')
        negative_list = driver.find_elements_by_xpath('//a[contains(@aria-hidden,"true")]')

        result_list = [item for item in positive_list if item not in negative_list and item in positive2_list ]


        content = driver.page_source
        soup = BeautifulSoup(content)
        date='none'
        if list_str(soup.find_all(attrs={"class":'_3JxPDYSx'})) is not None:
            date=list_str(soup.find_all(attrs={"class":'_3JxPDYSx'}))
        # print('d')
        # print(date)
        # display(date)
        dates= [y for x in [dates, date] for y in x]
        x=soup.find_all(attrs={"target":'_self'})
        ides=[]
        for i in range(len(x)):
            if not x[i].has_key('aria-hidden') and  x[i].has_key('href'):
                if '/Profile' in x[i]['href']:
                    ides.append(x[i].text)
        if len(ides)>10:
            ides=ides[:10]
        # display(ides) 
        idess= [y for x in [idess, ides] for y in x]

        x=soup.find_all(attrs={"width":88})
        likes=[]
        for i in range(len(x)):
            if x[i].has_key('aria-label') :
                likes.append(x[i]['aria-label'])
        # if len(ides)>10:
        likes=likes[2:12]
        # display(likes) 
        likess=[y for x in [likess, likes] for y in x]

        title=list_str(soup.find_all(attrs={"class":"_2tsgCuqy"}))[0::2]
        if len(title)>10:
            title=list_str(soup.find_all(attrs={"class":"_2tsgCuqy"}))[1::2]
        
            titles=[y for x in [titles, title] for y in x]
            mesage=list_str(soup.find_all(attrs={"class":"_2tsgCuqy"}))[2::2]
            mesages=[y for x in [mesages, mesage] for y in x]
        else:    
            titles=[y for x in [titles, title] for y in x]
            mesage=list_str(soup.find_all(attrs={"class":"_2tsgCuqy"}))[1::2]
            mesages=[y for x in [mesages, mesage] for y in x]
        


    #     print(result_list)
        for i in range(min(len(result_list),10)):
#             try:
                result_list[i].send_keys(Keys.CONTROL + Keys.RETURN)

                chwd = driver.window_handles

                driver.switch_to.window(chwd[1])
                time.sleep(1)


                content = driver.page_source
                soup = BeautifulSoup(content)

                if len(soup.find_all(attrs={"class":'errHdr'}))>0:
                    driver.close();
                    chwd = driver.window_handles
                    driver.switch_to.window(chwd[0])
                    level=0
                    detail=['0','0','0']
                    details.append(detail)
                    levels.append(level)
                    continue

                sleeper=10
                while True:
                    time.sleep(1)
                    content = driver.page_source
                    soup = BeautifulSoup(content)
                    detail=list_str(soup.find_all(attrs={"class":"iX3IT_XP"}))
                    sleeper=sleeper-1
                    if len(detail)==3 or sleeper==0:
                        break
                if sleeper==0:
                    detail=['0'] + detail
#                 print(detail)


                while True:
                    time.sleep(1)
                    try:
                        driver.find_element_by_xpath('//a[contains(@data-tab-name,"Badges")]').click()
                        break
                    except:
                        driver.find_element_by_xpath('//button[text()="Try again"]').click()
                    
                chwd = driver.window_handles
                driver.switch_to.window(chwd[2])
                content = driver.page_source
                soup = BeautifulSoup(content)
                try:
                    level=int(soup.find_all(attrs={"data-info-layout": "FlyoutRight"})[1].find('span').text)
                except:
                    level=0

                driver.close();
                chwd = driver.window_handles
                driver.switch_to.window(chwd[1])
                driver.close();
                chwd = driver.window_handles
                driver.switch_to.window(chwd[0])
                details.append(detail)
                levels.append(level)
#             except:
#                 pass
        elemans=driver.find_elements_by_xpath('//div[contains(@class,"_3djM0GaD")]')
        ss=len(elemans)
        next_b=elemans[-1]
        if first==1 or ss==2:
            while(True):
                try:
                    next_b.click()
                    first=0
                    break;
                except:
                    time.sleep(1)
        else:
            break
#     print(details)
#     print(np.array(details)[:,0])
#     print(np.transpose([np.array(levels)]))
# #     print(np.transpose([np.array(dates)]))
#     print(np.transpose([np.array(idess)]))
#     print(np.transpose([np.array(likess)]))
#     print(np.transpose([np.array(titles)]))
#     print(np.transpose([np.array(mesages)]))
        

    all_data=np.concatenate((np.array(details),np.transpose([np.array(levels)]),np.transpose([np.array(idess)]),np.transpose([np.array(likess)]),np.transpose([np.array(titles)]),np.transpose([np.array(mesages)])),axis=1)
    df = pd.DataFrame(data=all_data, columns=['Contributions','Followers','Following','levels','idess','likess','titles','mesages'])                    
     
    df.to_csv(name+'_do.csv')
    