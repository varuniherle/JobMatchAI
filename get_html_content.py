from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time



# this will get the entire content of the webpage 
def get_url_data(base_url):
    driver = webdriver.Chrome()
    driver.get(base_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup







    



