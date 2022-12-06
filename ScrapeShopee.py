import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import random

# added for streamlit deployment
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class ScrapeData():

    def __init__(self):  #class must have constructor
        pass

    def get_url(self, product):
        product = product.replace(" ",'%20')
        template = 'https://shopee.com.my/search?keyword={}'
        url = template.format(product)
        return url

    def get_all_products(self, card): #call function
        
        product_img = card.find_element(By.TAG_NAME, 'img')
        pImg = product_img.get_attribute('src')    

        product_name = card.find_element(By.CLASS_NAME,'Cve6sh').text.encode(encoding='ascii',errors= 'ignore').decode()

        product_price = card.find_element(By.CLASS_NAME,'ZEgDH9').text.strip()

        try:
            product_sold = card.find_element(By.CLASS_NAME,'r6HknA').text.strip()
        except AttributeError:
            product_sold = '0 sold'

        product_link = card.find_element(By.TAG_NAME, 'a')
        pLink = product_link.get_attribute('href')

        product_info = (pImg, product_name, product_price, product_sold, pLink)
        return product_info

    def scrape_process(self, product, no_prod):
        records = []
        scraped_count = 0 
        url = self.get_url(product) # since the file is a class, we add a "self." to call the function within the same class

        # added for streamlit deployment
        options = Options()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)

        btn = driver.find_element("xpath",'//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button')
        btn.click()
        sleep_time = random.randint(5,7) 
        time.sleep(sleep_time) 

        btn = driver.find_element("xpath", '//*[@id="main"]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[3]')  #click to top sales
        btn.click() 
        sleep_time = random.randint(5,7) 
        time.sleep(sleep_time) 

        # for i in range (1,3):            #use to set scraped pages
        while True:
            #Define an initial value
            temp_height=0
    
            while True:
                #Looping down the scroll bar
                driver.execute_script("window.scrollBy(0,1000)")
                #sleep and let the scroll bar react
                time.sleep(5)
                #Get the distance of the current scroll bar from the top
                check_height = driver.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
                #If the two are equal to the end
                if check_height==temp_height:
                    break
                temp_height=check_height

            
            product_cards = driver.find_elements(By.CLASS_NAME, 'col-xs-2-4')

            for everyProduct in product_cards:
                productDetails = self.get_all_products(everyProduct) # since the file is a class, we add a "self." to call the function within the same class
                records.append(productDetails)
                
                scraped_count += 1
                print("scrapped_count",  scraped_count)
                print("no_prod",  no_prod)

                if scraped_count == int(no_prod):
                    print('done')
                    driver.quit()
                    return records    


    def main(self, product, no_prod):
        records = self.scrape_process(product, no_prod)

        col = ['Product_Image','Product_Name','Product_Price','Product_Sold','Product_Buy_Link']
        shopee_data = pd.DataFrame(records,columns=col)
        shopee_data.to_csv('ShopeeData.csv')