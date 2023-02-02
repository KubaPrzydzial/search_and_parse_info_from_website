from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time
# from datetime import datetime

# start_time = datetime.now()

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
driver.maximize_window()
driver.get("url")

# open the file with brand names
with open("brandy.txt", "r", encoding='utf-8') as file:
    brands = file.readlines()
    # Loop over each brand
    for brand in brands:
        # accept cookies
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Tak, zgadzam się')]"))).click()
        except:
        # if not found just carry on
            pass

        try:
            # pick category
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Męskie')]"))).click()
        except:
            pass

        search_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located(("id", "brands-autocomplete")))
        search_field.clear()
        search_field.send_keys(brand)

        link = None
        try:
            link = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='brands-autocomplete-menu-item-0']")))
        except:
            # if not found, go back to start of the loop
            continue

        if link:
            link.click()
            try:
                button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Dalej')]"))).click()
            except:
                continue

        try:
            link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, ".//*[@id='category-54']"))).click()
            # time.sleep(3)
        finally:
            link = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Kurtka (skóra naturalna)')]")))
            link.click()

        try:
            # locate the elements to be saved
            brand_id_element = driver.find_element("id", "brand-crumb")
            brand_name = brand_id_element.get_attribute("data-gtm-brand") ### brand name
            brand_id = brand_id_element.get_attribute("data-gtm-brand-id") ### brand id
            price_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'price py-4')]")))  ### locate price element
            price = price_element.text ### price
            price_replaced = price.replace('zł', 'PLN')
            # write the brand, brand_id, and price to a CSV file
            with open("output.csv", "a", newline="", encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([brand_name, brand_id, price_replaced])

        finally:
            driver.get("url")

# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))
# Close the WebDriver
driver.close()
