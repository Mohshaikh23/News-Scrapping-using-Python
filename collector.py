from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup


#Load your CSV file into a DataFrame
df = pd.read_csv("Data.csv")

#Limit the scrapping news as per your requirement
df = df[:51]

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Create a new column in the DataFrame to store the article content
df['Article_Content'] = ''

# Iterate through each link in the DataFrame
for index, link in enumerate(df["Links"]):
    driver.get(link)

    # Give the page time to load 
    time.sleep(3)  
    
    content = driver.find_element(By.ID, 'main-content')
    data = content.get_attribute("outerHTML")

    soup = BeautifulSoup(data, "html.parser")
    content_paragraphs = [line.get_text() for line in soup.find_all("p", attrs={'class': 'sc-eb7bd5f6-0 fYAfXe'})]

    article_content = ''
    for paragraph in content_paragraphs:
        paragraph = paragraph.replace("�", "'")
        article_content += paragraph

    # Add the article content to the corresponding row in the DataFrame
    df.at[index, 'Article_Content'] = article_content

# Close the WebDriver
driver.quit()

# Save the updated DataFrame back to a CSV file
df.to_csv("Updated_Data.csv", index=False)
