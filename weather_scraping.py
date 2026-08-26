import json
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# options = webdriver.ChromeOptions()

# options.add_argument(
#     "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) "
#     "Chrome/151.0.0.0 Safari/537.36"
# )

# driver = webdriver.Chrome(
#     service=ChromeService(ChromeDriverManager().install()),
#     options=options
# )

# capitals_climate_URL = "https://www.timeanddate.com/weather/?low=c"


# try:
#     driver.get(capitals_climate_URL)
   
#     capitals_table = driver.find_element(By.CSS_SELECTOR, '.zebra.fw.tb-theme')
   
    
#     cities = capitals_table.find_elements(By.CSS_SELECTOR, 'td a[href^="/weather/"]')
#     capitals_list = []
 
#     for city in cities:
#         href = city.get_attribute("href")
#         capitals_list.append({"City":city.text,
#                                "Link": href })

#     print(capitals_list)





  
# except Exception as e:
#     print("couldn't get the web page")
#     print(f"Exception: {type(e).__name__} {e}")

# finally:
#     driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.page_load_strategy = "eager"

driver = webdriver.Chrome(options=options)

try:
    driver.set_page_load_timeout(30)

    driver.get("https://www.timeanddate.com/weather/?low=c")

    print("Page loaded!")
    print(driver.title)

    cities = driver.find_elements(
    By.XPATH,
    '//table[contains(@class, "zebra")]//td/a[@href]'
)

    capitals_list = []

    for city in cities:
        capitals_list.append({
            "City": city.text,
            "Link": city.get_attribute("href")
        })
    

    print(capitals_list)

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

            climate_monthly.append({
                "City": city,
                "Month": month_name,
                "High Temp": high_temp,
                "Low Temp": low_temp,
                "Mean Temp": mean_temp,
                "Precipitation": precipitation,
        
            })
        return climate_monthly

    capitals_climate_monthly = []
    for city in capitals_list:
        city_name = city["City"]
        city_climate_URL = city["Link"]+"/climate"
        climate_monthly =  scrape_monttly_weater_by_city(driver, city_name, city_climate_URL)
        capitals_climate_monthly.extend(climate_monthly)
        print(capitals_climate_monthly[0:50])



    climate_df = pd.DataFrame(capitals_climate_monthly)
    climate_df.to_csv("climate_data.csv", index=False)
finally:
    driver.quit()