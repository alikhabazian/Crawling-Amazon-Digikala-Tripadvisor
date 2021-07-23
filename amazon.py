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
import re
from IPython.display import clear_output



def list_str(lis):
    q=[]
    for i in range(len(lis)):
        q.append(lis[i].text.strip())
    return q


def amazon(Link,number_page):
    
    try:
        link=Link
#         link="https://www.amazon.com/TOZO-T6-Bluetooth-Headphones-Waterproof/dp/B07RGZ5NKS/ref=cm_cr_arp_d_product_top?ie=UTF8"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(link)

        content = driver.page_source
        soup = BeautifulSoup(content)

        element=driver.find_element_by_xpath("//a[@data-hook = 'see-all-reviews-link-foot']")
        while(True):
            try:
                ActionChains(driver).move_to_element(element).click().perform()
                break
            except:
                time.sleep(1)
        count=0
        page_reviews=[]
        reviews_dates=[]
        reviews_stars=[]
        review_titles=[]
        profile_names=[]
        content = driver.page_source
        soup = BeautifulSoup(content)
        name=soup.find(attrs={"data-hook": "product-link"}).text
        rate=soup.find(attrs={"data-hook": 'rating-out-of-text'}).text
        star5=soup.find_all( attrs={'title': re.compile(r'^5 stars r')})[2].text.strip()
        star4=soup.find_all( attrs={'title': re.compile(r'^4 stars r')})[2].text.strip()
        star3=soup.find_all( attrs={'title': re.compile(r'^3 stars r')})[2].text.strip()
        star2=soup.find_all( attrs={'title': re.compile(r'^2 stars r')})[2].text.strip()
        star1=soup.find_all( attrs={'title': re.compile(r'^1 stars r')})[2].text.strip()
        stars=[star1, star2, star3, star4 ,star5]
        while(True):
            clear_output(wait=True)
            count=count+1
            print(count)
            content = driver.page_source
            soup = BeautifulSoup(content)


            page_review=list_str(soup.find_all(attrs={"data-hook":"review-body"}))
            reviews_date=list_str(soup.find_all(attrs={"data-hook":"review-date"}))
            reviews_star=list_str(soup.find_all(attrs={"data-hook":"review-star-rating"})+soup.find_all(attrs={"data-hook":"cmps-review-star-rating"}))
            review_title=list_str(soup.find_all(attrs={"data-hook":"review-title"})[2:])
            profile_name=list_str(soup.find_all(attrs={"class":"a-profile-name"})[2:])
            page_reviews = np.concatenate((page_reviews, page_review))
            reviews_dates=np.concatenate((reviews_dates, reviews_date))
            reviews_stars=np.concatenate((reviews_stars, reviews_star))
            review_titles=np.concatenate((review_titles, review_title))
            profile_names=np.concatenate((profile_names, profile_name))
            time.sleep(1)
            if(len(soup.find_all(attrs={"class":"a-last"}))==0 or count==number_page):
                break
            while(True):
                try:
                    element=driver.find_element_by_xpath("//*[text()='Next page']")
                    break
                except:
                    time.sleep(1)
            while(True):
                try:
                    ActionChains(driver).move_to_element(element).click().perform()
                    break
                except:
                    time.sleep(1)
#         print(1)
#         print(len(np.transpose([np.array(page_reviews)])))
#         print(len(np.transpose([np.array(reviews_dates)])))
#         print(reviews_stars)
#         print(len(np.transpose([np.array(reviews_stars)])))
        
        all_data=np.concatenate((np.transpose([np.array(page_reviews)]),np.transpose([np.array(reviews_dates)]),np.transpose([np.array(reviews_stars)]),np.transpose([np.array(review_titles)]),np.transpose([np.array(profile_names)])),axis=1)
#         print(2)
        df = pd.DataFrame(data=all_data, columns=['page_reviews','reviews_dates','reviews_stars','review_titles','profile_names'])   
        print(name+'.csv')
        df.to_csv(name+'.csv')
    except ValueError:
            print(ValueError)