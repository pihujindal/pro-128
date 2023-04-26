from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

START_URL="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser=webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)
scraped_data=[]

def scrape():

        
        soup=BeautifulSoup(browser.page_source,'html.parser')
        #find table
        bright_star_table = soup.find("table",attrs={"class","wikitable"})
        #find <tbody>
        table_body = bright_star_table.find('tbody')
        #find <tr>
        table_rows = table_body.find_all("tr")

        # get data from td
        for row in table_rows:
            table_cols = row.find_all('td')
            #print(table_cols)
            temp_list=[]

            for col_data in table_cols:
                data=col_data.text.strip()
                #print(data)
                temp_list.append(data)
                scraped_data.append(temp_list)
star_data=[]
for i in range(0,len(scraped_data)):
    Star_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]

    require_data  = [Star_names,Distance,Mass,Radius,Lum]
    star_data.append(require_data)

headers=['star_name','Distance','Mass','Radius','Luminosity']
star_df_1 = pd.DataFrame(star_data,columns=headers)
star_df_1.to_csv('scraped_data.csv',index=True,index_label='id')


