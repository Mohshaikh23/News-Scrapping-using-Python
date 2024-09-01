from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time
from bs4 import BeautifulSoup

# Data Scrapping
driver= webdriver.Chrome()

try:
    page_number = 1
    driver.get("https://www.bbc.com/")
    element= driver.find_element(By.XPATH, 
                                    '//button[@aria-label="Search BBC"]')
    element.click()
    delement = driver.find_element(By.XPATH,
                                '//*[@id="__next"]/div/div[6]/div/div[1]/div/input')
    delement.send_keys("Technology")
    delement.send_keys(Keys.RETURN) 
    while True:
        tech_element = driver.find_element(By.XPATH,
                                            '//*[@id="main-content"]/div[1]/div/div[2]/div')
        data = tech_element.get_attribute("outerHTML")
        with open("News.html","a") as f:
            f.write(data)

        next_page = driver.find_element(By.XPATH,'//button[@aria-label="Next Page"]')
        next_page.click()
        page_number += 1

except Exception as e:
    print(e)

finally:
    time.sleep(2)
    driver.quit()

# Data Extraction
data_dict= {"time_ago":[],
            "titles":[],
            "subtitles":[],
            "location":[],
            "images":[],
            "Links":[]} 

with open("News.html",'r') as f:
    html_doc = f.read()
    soup= BeautifulSoup(html_doc,"html.parser")
    time_ago = soup.find_all("span",attrs={'class':'sc-4e537b1-1 dkFuVs'})
    titles = soup.find_all("h2")
    subtitles = soup.find_all("p")
    location = soup.find_all("span",attrs={'class':'sc-4e537b1-2 eRsxHt'})
    images = [img['src'] for img in soup.find_all("img")]
    links = [link['href'] for link in soup.find_all("a")]

    for time_ago,title,subtitle,location,image,link in zip(time_ago,titles,subtitles,location,images,links):
        data_dict["time_ago"].append(time_ago.get_text().strip())
        data_dict["titles"].append(title.get_text().strip())
        data_dict["subtitles"].append(subtitle.get_text().strip())
        data_dict["location"].append(location.get_text().strip())
        data_dict["images"].append(image)
        data_dict["Links"].append("https://www.bbc.com"+link)
        
df = pd.DataFrame(data_dict)
for i in df.columns:
    df[i]= df[i].str.strip().str.split().str.join(' ')

df.to_csv("Data.csv")

