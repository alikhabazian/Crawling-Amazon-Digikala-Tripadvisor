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

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 
        
def digikala_comment_getter(link,number_page):

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(link)

        content = driver.page_source

        soup = BeautifulSoup(content)
        filename=soup.find(attrs={"title"}).text+".csv"
        all1=soup.find_all(attrs={"class": "c-comments__item c-comments__item--pdp"})
        goal=[]
        for element in all1:
            title=None if element.find(attrs={"class": "c-comments__title"}) == None else element.find(attrs={"class": "c-comments__title"}).text
            date=element.find_all(attrs={"class": "c-comments__detail"})[0].text
            who=element.find_all(attrs={"class": "c-comments__detail"})[1].text
            suggest=element.find(attrs={"class": "c-comments__status c-comments__status--positive"})!=None
            nosuggest=element.find(attrs={"class": "c-comments__status c-comments__status--negetive"})!=None
            content=element.find(attrs={"class": "c-comments__content"}).text
            color=None if element.find(attrs={"class": "c-comments__color"}) == None else element.find(attrs={"class": "c-comments__color"}).text.replace('\n', '').replace(' ', '')
            seller=None if element.find(attrs={"class": "c-comments__seller"})== None else element.find(attrs={"class": "c-comments__seller"}).text
            goods=[]
            g=element.find_all(attrs={"class": "c-comments__modal-evaluation-item--positive"})
            for l in g:
                goods.append(l.text.replace('\n', '').replace('                                ',"").replace('                            ',""))
                goods.append('،')

            good=None if len(goods)==0 else listToString(goods)
            like='0' if element.find(attrs={"class": "c-comments__helpful-yes js-comment-like"})== None else element.find(attrs={"class": "c-comments__helpful-yes js-comment-like"}).text
            dislike='0' if element.find(attrs={"class": "c-comments__helpful-no js-comment-dilike"})== None else element.find(attrs={"class": "c-comments__helpful-no js-comment-dilike"}).text
            goal.append([title,date,who,suggest,nosuggest,content,color,seller,good,like,dislike])
        last_page=int(soup.find(attrs={"id": "comment-pagination"}).find(attrs={"class","c-pager__items"}).find(attrs={"class": "c-pager__next"})["data-page"])
        now=2
        while(now<=min(number_page,last_page)):
            clear_output(wait=True)
            print(now)
            print(':')


            element=driver.find_element_by_xpath("//a[@data-page = '{}']".format(now))
            while(True):
                try:
                    ActionChains(driver).move_to_element(element).click().perform()
                    break



                except:
                    time.sleep(2)








            content = driver.page_source

            soup = BeautifulSoup(content)
            all1=soup.find_all(attrs={"class": "c-comments__item c-comments__item--pdp"})
            for element in all1:
                title=None if element.find(attrs={"class": "c-comments__title"}) == None else element.find(attrs={"class": "c-comments__title"}).text
                date=element.find_all(attrs={"class": "c-comments__detail"})[0].text
                who=element.find_all(attrs={"class": "c-comments__detail"})[1].text
                suggest=element.find(attrs={"class": "c-comments__status c-comments__status--positive"})!=None
                nosuggest=element.find(attrs={"class": "c-comments__status c-comments__status--negetive"})!=None
                content=element.find(attrs={"class": "c-comments__content"}).text
                color=None if element.find(attrs={"class": "c-comments__color"}) == None else element.find(attrs={"class": "c-comments__color"}).text.replace('\n', '').replace(' ', '')
                seller=None if element.find(attrs={"class": "c-comments__seller"})== None else element.find(attrs={"class": "c-comments__seller"}).text
                goods=[]
                g=element.find_all(attrs={"class": "c-comments__modal-evaluation-item--positive"})
                for l in g:
                    goods.append(l.text.replace('\n', '').replace('                                ',"").replace('                            ',""))
                    goods.append('،')

                good=None if len(goods)==0 else listToString(goods)
                like='0' if element.find(attrs={"class": "c-comments__helpful-yes js-comment-like"})== None else element.find(attrs={"class": "c-comments__helpful-yes js-comment-like"}).text
                dislike='0' if element.find(attrs={"class": "c-comments__helpful-no js-comment-dilike"})== None else element.find(attrs={"class": "c-comments__helpful-no js-comment-dilike"}).text
                goal.append([title,date,who,suggest,nosuggest,content,color,seller,good,like,dislike])
            now=now+1
        data_np=np.array(goal)
        df = pd.DataFrame(data=data_np, columns=['title','date','who','suggest','nosuggest','content','color','seller','good','like','dislike'])
        
        df.to_csv(filename.replace('/','_').replace('\t', ''), encoding="utf-8-sig", index = False)
        print("saved in {}".format(filename))
    except ValueError:
        print(ValueError)

