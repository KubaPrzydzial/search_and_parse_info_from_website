from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time

# open the file with brand names
with open("brandy.txt", "r") as file:
    brands = file.readlines()

# create webdriver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.maximize_window()

# go to website
driver.get("url")


# Loop over each brand
for brand in brands:
    brand = brand.strip()

    # accept cookies
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Tak, zgadzam się')]"))).click()
    except:
    # if not found just carry on
        pass

    try:
        # pick category
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Męskie')]"))).click()
    except:
        pass

    # find search field and input brand name
    try:
        search_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located(("id", "brands-autocomplete")))
        search_field.send_keys(brand)
        time.sleep(3)
        search_field.send_keys(Keys.RETURN)
    except:
        # if not found, skip to next brand
        search_field.clear()

    try:
        button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Dalej')]"))).click()
    except:
        continue

    try:
        link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='category-54']"))).click()
        time.sleep(3)
    finally:
        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Kurtka (skóra naturalna)')]")))
        link.click()

    try:
        # locate the elements to be saved
        brand_id_element = driver.find_element("id", "brand-crumb")
        brand_name = brand_id_element.get_attribute("data-gtm-brand") ### brand name
        brand_id = brand_id_element.get_attribute("data-gtm-brand-id") ### brand id
        price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'price py-4')]")))  ### locate price element
        price = price_element.text ### price
        # write the brand, brand_id, and price to a CSV file
        with open("output.csv", "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([brand_name, brand_id, price])

    finally:
        driver.get("url")

# Close the WebDriver
driver.close()
