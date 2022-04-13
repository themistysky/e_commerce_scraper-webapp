'''Module for Scraper class.'''

import time
import os
import re
import warnings
import requests
from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup as bs4
warnings.filterwarnings('ignore')
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.chrome.options import Options
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pandas import DataFrame
import random as rn
from undetected_chromedriver import Chrome
rn.seed(120)
links = ['https://www.kotsovolos.cy/',
             'https://www.kotsovolos.gr/',
             'https://www.plaisio.gr/',
             'https://www.mediamarkt.gr/',
             'https://www.public.cy/',
             'https://www.public.gr/',
             'https://www.stephanis.com.cy/',
             'https://www.electroline.com.cy/',
             'https://sofroniouelectronics.com/index.php',
             'http://www.cosmodata.gr/',
    ]


def get_driver():
    options = ChromeOptions()
    options.add_argument("start-maximized")
#    options.add_argument('--disable-blink-features=AutomationControlled')
#    options.headless=True
#    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    # chrome_path = '/home/akash/scraping_app_env/lib/python3.8/site-packages/chromedriver_binary/chromedriver'
    options.headless = True
    # remove the executable_path argument while running on windows
    ex_path =  '/home/scraper/scraping_app/chromedriver'
    driver = Chrome(executable_path = ex_path, options=options)
    return driver

class Scraper:
    
    def __init__(self, keywords, websites):
        self.websites = websites
        self.keywords = keywords
        self.result = DataFrame(columns = ['keywords','website','title','price','availability'])


    def scrape(self):

        for website in self.websites:
            print(f"Starting scraping '{self.keywords}' from", website)
            
            try:
                if website == links[0]:
                    self.from_kotsov_cy()
                    
                elif website == links[1]:
                    self.from_kotsov_gr()
                    
                elif website == links[2]:
                    self.from_plaisio_gr()

                elif website == links[3]:
                    self.from_mediamarket_gr()

                elif website == links[4]:
                    self.from_public_cy()

                elif website == links[5]:
                    self.from_public_gr()

                elif website == links[6]:
                    self.from_stephanis_cy()

                elif website == links[7]:
                    self.from_electro_cy()

                elif website == links[8]:
                    self.from_sofron_com()

                elif website == links[9]:
                    self.from_cosmo()

                print("Scraping", website, "done")

            except Exception as e:
                raise e
                print(f"Error while scraping {repr(self.keywords)} from {website}")

            print(len(self.result))


    def from_kotsov_gr(self):
        website = 'https://www.kotsovolos.gr/'
        key = self.keywords.replace(' ','+')
        pg = 0
        link = f'https://www.kotsovolos.gr/SearchDisplay?q={key}&l=60&storeId=10151'
        driver = get_driver()
        driver.get(link)
        time.sleep(6)

        try:
            lastpg = int(driver.find_element_by_class_name('pagination').find_elements_by_tag_name('a')[-2].text)
        except:
            lastpg = 0
        print('lastpg', lastpg)
        while pg<lastpg:
            if pg>0:
                link = f'https://www.kotsovolos.gr/SearchDisplay?q={key}&l=60&o={str(pg*60)}&storeId=10151'
                driver.get(link)
                time.sleep(rn.random()*3)

            html = driver.page_source
            soup = bs4(html,'html.parser')
            prods = soup.find_all('div', class_='product')
            for prod in prods:
                price_eles = prod.find_all('span', class_='main-price')
                try:
                    price = price_eles[0].parent.get_text().strip()
                    availability = prod.find('div', class_='availability__title').get_text().strip() if prod.find('div', class_='availability__title') else ''
                    title = prod.find('div', class_ = 'title').get_text().strip()
                    self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                except:
                    pass
            
            pg+=1


    def from_kotsov_cy(self):
        website = 'https://www.kotsovolos.cy/'
        driver = get_driver()
        key = self.keywords.replace(' ', '+')
        link = f'https://www.kotsovolos.cy/SearchDisplay?storeId=10161&searchTerm={key}'
        driver.get(link)
        time.sleep(5)
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))).click()
        time.sleep(2)

        while 1:
            html = driver.page_source
            soup = bs4(html,'html.parser')
            prods = soup.find_all('div', class_='product')
            
            for prod in prods:
                price_eles = prod.find_all('span', class_='main-price')
                try:
                    price = price_eles[0].parent.get_text().strip()
                    availability = prod.find('div', class_='availability__title').get_text().strip() if prod.find('div', class_='availability__title') else ''
                    #vatlessprice = price_eles[1].parent.get_text().strip() if len(price_eles)>1 else None
                    title = prod.find('div', class_ = 'title').get_text().strip()
                    self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                except Exception as e:
                    print(e)
                    pass
                
            start = 0
            end = 0
            while start<2:
                try:
                    nexturl = driver.find_element_by_xpath('/html/body/main/div/div[2]/div[2]/section/div[6]/div[2]/ul/li[@class="active"]/following-sibling::li/a').get_attribute('href')
                    print('nexturl',nexturl)
                    if not nexturl:
                        end = 1
                        break
                    driver.get(nexturl)
                    time.sleep(float(str(rn.random())[:4])*6)
                    break
                except:
                    print('click fail')
                    start+=1
                    time.sleep(3)
            print(len(self.result))
            if start==2 or end: break

        # totalpgs = soup.find('ul', class_='pagination').find_all('li')[-2].text
        # print(totalpgs)


    def from_plaisio_gr(self):
        website = 'https://www.plaisio.gr/'
        key = self.keywords.replace(' ','%20')
        page = '1'
        link = f'https://www.plaisio.gr/search?query={key}&page={page}&hitsPerPage=2000'
        driver = get_driver()
        
        driver.get(link)
        time.sleep(4)
        # WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))).click()
        html = driver.page_source
        soup = bs4(html,'html.parser')
        prods = soup.find_all('div', class_ ='product')

        for prod in prods:

            try:
                price = prod.find('div', class_='price').find('div', class_='price').text.strip()
                title = prod.find('span', class_ = 'product-title').get_text().strip()
                availability = prod.find('span', class_='stock-indication-text').text.strip() if prod.find('span', class_='stock-indication-text') else ''
                # print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
                self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
            except:
                pass



    def from_public_cy(self):
        website = 'https://www.public.cy/'
        key = self.keywords.replace(' ','%20')
        link = f'https://www.public.cy/search?q={key}&r=1500'
        
        driver = get_driver()
        driver.get(link)
        time.sleep(8)

        last_height = driver.execute_script("return document.body.scrollHeight")
        h=0
        while h <= int(last_height)+600:
            driver.execute_script(f"window.scrollTo(0, {str(h)});")
            h+=200
            time.sleep(float(str(rn.random())[:4])/3)
            
        html = driver.page_source
        soup = bs4(html,'html.parser')
        prods = soup.find_all('article', class_ ='product--grid')

        for prod in prods:
            try:
                price = prod.find('div', class_='product__price--final').text.strip()
                title = prod.find('h3', class_ = 'product__title').get_text().strip()
                availability = prod.find('div', class_='mdc-typography--caption').text.strip() if prod.find('div', class_='mdc-typography--caption') else ''
                self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                # print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')

            except:
                pass


    def from_public_gr(self):
        website = 'https://www.public.gr/'
        key = self.keywords.replace(' ', '%20')
        driver = get_driver()
        link = f'https://www.public.gr/search?q={key}&r=1000'

        driver.get(link)
        time.sleep(3)
        #WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))).click()

        last_height = driver.execute_script("return document.body.scrollHeight")
        h=0
        while h <= int(last_height)+1200:
            driver.execute_script(f"window.scrollTo(0, {str(h)});")
            h+=1000
            time.sleep(float(str(rn.random())[:4])/3)
            
        html = driver.page_source
        soup = bs4(html,'html.parser')
        prods = soup.find_all('article', class_ ='product--grid')

        for prod in prods:
            try:
                price = prod.find('div', class_='product__price--final').text.strip()
                title = prod.find('h3', class_ = 'product__title').get_text().strip()
                availability = prod.find('div', class_='mdc-typography--caption').text.strip()
                self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                # print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
            except Exception as e:
                print(e)
                pass
        driver.close()


    def from_mediamarket_gr(self):
        website = 'https://www.mediamarkt.gr/'
        key = self.keywords.replace(' ','%20')
        pg = 1
        link = f'https://www.mediamarkt.gr/search?query={key}&page={str(pg)}'
        driver = get_driver()
        
        driver.get(link)
        time.sleep(2)
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID,"CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"))).click()
        last_height = driver.execute_script("return document.body.scrollHeight")
        lastpg = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CLASS_NAME,'ngx-pagination'))).find_elements_by_tag_name('li')[-2].text
        lastpg = int(re.search('\d+', lastpg).group() if re.search('\d+', lastpg) else 1)
        print(lastpg)

        while pg <= lastpg:
            if pg != 1:
                driver.get(link)
            h=0
            while h<=int(last_height)+600:
                driver.execute_script(f"window.scrollTo(0, {str(h)});")
                h+=200
                time.sleep(rn.random())
            html = driver.page_source
            soup = bs4(html,'html.parser')
            prods = soup.find_all('article', class_ ='article--product')

            for prod in prods:
                try:
                    price = prod.find('div', class_='article__price').text.strip().split()[-1]
                    title = prod.find('h3', class_ = 'article__title').get_text().strip()
                    availability = prod.find('span', class_=['text-success','text-danger']).text.strip()
                    self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                    #print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
                except:
                    pass
            
            time.sleep(rn.random()*3)
            pg+=1
            link = f'https://www.mediamarkt.gr/search?query={key}&page={str(pg)}'
            



    def from_stephanis_cy(self):
        website = 'https://www.stephanis.com.cy/'
        key = self.keywords.replace(' ','+')
        pg = 1
        link = f'https://www.stephanis.com.cy/search?q={key}&page={str(pg)}/&recordsPerPage=2000'
        driver = get_driver()

        driver.get(link)
        time.sleep(4)

        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME,"consent-all-trigger"))).click()

        try:
            allpgs = driver.find_element_by_class_name('page-selection-list').find_elements_by_tag_name('li')
            allpgs = [x.find_element_by_tag_name('a').get_attribute('href') for x in allpgs]

        except:
            allpgs = [link]

        print(len(allpgs))

        for pg, link in enumerate(allpgs):
            if not pg:
                driver.get(link)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            html = driver.page_source
            soup = bs4(html,'html.parser')

            prods = soup.find_all('div', class_ ='item-wrapper') 

            for prod in prods:
                try:
                    price = prod.find('div', class_='with-sale').text.strip().split()[-1]
                    title = prod.find('li', class_ = 'tile-product-name').get_text().strip()
                    availability = prod.find('div', class_='product-availability').text.strip()
                    self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                    #print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
                except:
                    pass

            time.sleep(rn.random()*3)


    def from_electro_cy(self):
        website = 'https://www.electroline.com.cy'
        key = self.keywords.replace(' ', '+')
        pg = 1
        link = f'https://www.electroline.com.cy/page/{str(pg)}/?s={key}&post_type=product&lang=el'
        driver = get_driver()

        driver.get(link)
        time.sleep(4)

        try:
            lastpg = driver.find_elements_by_xpath('//a[@class="page-numbers"]')[-1].text
        except:
            lastpg = ''

        lastpg = int(re.search('\d+', lastpg).group() if re.search('\d+', lastpg) else 1)
        print(lastpg)

        while pg<=lastpg:
            if pg!=1:
                driver.get(link)
                
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            html = driver.page_source
            soup = bs4(html,'html.parser')

            prods = soup.find_all('li', class_ ='listing-product') 

            for prod in prods:
                try:
                    price = prod.find('div', class_='listing-product-price').text.strip().split()[-1]
                    title = prod.find('h3', class_ = 'listing-product__title').get_text().strip()
                    availability = prod.find('p', class_='listing-product-availability-text').text.split('\n')[-1].strip()
                    self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                    #print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
                except:
                    pass
            
            pg+=1
            link = f'https://www.electroline.com.cy/page/{str(pg)}/?s={key}&post_type=product&lang=el'


    def from_sofron_com(self):
        website = 'https://sofroniouelectronics.com/index.php'
        key = self.keywords.replace(' ','+')
        pg = 1
        link = f'https://sofroniouelectronics.com/index.php?controller=search&s={key}&page={str(pg)}'
        driver = get_driver()
        availability = ''

        driver.get(link)
        time.sleep(3)

        try:
            lastpg = int(driver.find_element_by_class_name('page-list').find_elements_by_tag_name('a')[-2].get_attribute('href')[-1])
        except:
            lastpg = 1
        num = 1
        pg = lastpg
        link = f'https://sofroniouelectronics.com/index.php?controller=search&s={key}&page={str(pg)}'
        driver.get(link)
        time.sleep(3)

        html = driver.page_source
        soup = bs4(html,'html.parser')
        prods = soup.find_all('div', class_ ='thumbnail-container')

        for prod in prods:
            try:
                price = prod.find('span', class_='price').text.strip().split()[-1]
                title = prod.find('h6').text.strip()
                self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                #print(num, 'Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\n')
                num+=1
            except:
                pass


    def from_cosmo(self):
        website = 'https://www.cosmodata.gr/'
        key = self.keywords
        driver = get_driver()

        key = 'iphone'.replace(' ', '+')
        link = f'https://www.cosmodata.gr/search?makers=&cat6=&aq={key}&ai=&prices=1_2055&sort=asc&storex=&items=1000'
        
        driver.get(website)
        time.sleep(3)
        
        driver.get(link)
        time.sleep(3)
        
        html = driver.page_source
        soup = bs4(html,'html.parser')

        prods = soup.find_all('div', class_ ='pd_div5') 

        for prod in prods:
            try:
                price = prod.find('div', class_='pd_price').text.strip().split()[-1]
                title = prod.find('div', class_='pd_title').text.strip()
                availability = prod.find('div', class_='diathe1').text.strip()
                self.result.loc[len(self.result)] = [ self.keywords, website, title, price, availability]
                # print('Title:',title if title else '_','\nPrice (with VAT):', price if price else '_','\nAvailability:',availability if availability else'_','\n')
            except:
                pass


        
# for testing
if __name__=='__main__':
    print("\n\nInside Main\n")
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    time.sleep(4)
    #keywords = input('Enter keywords: ')
    keywords = 'bluetooth headphones'
    websites = links[6:]

    scraper = Scraper(keywords, websites, driver)
    scraper.scrape()
    scraper.result.to_csv('result.csv', mode='w', index=False, encoding='utf-8')
    driver.quit()
