import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=options)

try:
    driver.set_page_load_timeout(30)
#load capitals page
    driver.get("https://www.timeanddate.com/weather/?low=c")

    print("Page loaded!")

    print(driver.title)
#load all the capitals 
    cities = driver.find_elements(
    By.XPATH,
    '//table[contains(@class, "zebra")]//td/a[@href]'
)
#create a list of all capitals
    capitals_list = []

    for city in cities:
        capitals_list.append({
            "City": city.text,
            "Link": city.get_attribute("href")
        })
    

    print(capitals_list)
#create a function that scrapes data for each capital for current month
    def scrape_monttly_weater_by_city(driver, city, url):
        climate_monthly = []
        driver.get(url)
  
        months = driver.find_elements(
        By.CSS_SELECTOR,
        '#climateTable .climate-month:not(.climate-month--allyear)'
    )


        for month in months:
            month_name = month.find_element(By.TAG_NAME, "h3").text.strip()
            if not month_name:
                continue
            month_name = month_name.split()[0]
            high_temp = month.find_element(
                 By.XPATH,
            ".//span[contains(text(), 'High Temp:')]/.."
        ).text.replace("High Temp: ", "").strip()
         #search inside the current element and all of its descendants for the text,
         # and after that text is found go to the parent element of this span
            low_temp = month.find_element(
            By.XPATH,
            ".//span[contains(text(), 'Low Temp:')]/.."
        ).text.replace("Low Temp: ", "").strip()
            mean_temp = month.find_element(
            By.XPATH,
            ".//span[contains(text(), 'Mean Temp:')]/.."
        ).text.replace("Mean Temp: ", "").strip()
            precipitation = month.find_element(
            By.XPATH,
            ".//span[contains(text(), 'Precipitation:')]/.."
        ).text.replace("Precipitation: ", "").strip()
 #add scarped data to the list
            climate_monthly.append({
                "City": city,
                "Month": month_name,
                "High Temp": high_temp,
                "Low Temp": low_temp,
                "Mean Temp": mean_temp,
                "Precipitation": precipitation,
        
            })
            sleep(1)
        return climate_monthly

    capitals_climate_monthly = []
    for city in capitals_list:
        city_name = city["City"]
        #create URL for each capital based on info we scraped and adding /climate
        city_climate_URL = city["Link"]+"/climate"
        #call created function with the url created for each city
        climate_monthly =  scrape_monttly_weater_by_city(driver, city_name, city_climate_URL)
        #take all the items from climate_monthly and add them to capitals_climate_monthly
        capitals_climate_monthly.extend(climate_monthly)
        #print(capitals_climate_monthly[0:50])

#create a df from this list of dict

    climate_df = pd.DataFrame(capitals_climate_monthly)
#write df to csv
    climate_df.to_csv("climate_data.csv", index=False)
finally:
    driver.quit()