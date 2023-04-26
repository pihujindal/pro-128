from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd


START_URL="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

browser=webdriver.Chrome("D:/Setup/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)
new_scraped_data=[]


def scrape_more_data(hyperlink):
    print(hyperlink)
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]

        for tr_tag in soup.find_all("tr",attrs={"class":"wikitable sortable jquery-tablesorter"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append()
        new_scraped_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
       
star_df_1 = pd.read_csv("scraped_data.csv")
# Call method
for index, row in star_df_1.iterrows():

     ## ADD CODE HERE ##
    print(row['hyperlink'])
     # Call scrape_more_data(<hyperlink>)
    scrape_more_data(row['hyperlink'])
    print(f"Data Scraping at hyperlink {index+1} completed")

print(new_scraped_data)

# Remove '\n' character from the scraped data
scraped_data = []

for row in new_scraped_data:
    replaced = []
    ## ADD CODE HERE ##
    for el in row:
        el=el.replace("\n","")
        replaced.append(el)
    
    scraped_data.append(replaced)

print(scraped_data)

headers = ["Brown dwarf","Constellation", "Right ascension", "Declination", "App. mag.", "Distance", "Spectral type", "Mass","Radius","Discovery year"]

new_planet_df_1 = pd.DataFrame(scraped_data,columns = headers)

# Convert to CSV
new_planet_df_1.to_csv('new_scraped_data.csv', index=True, index_label="id")

