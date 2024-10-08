import time
import os
import shutil
from pprint import pprint
import urllib.request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# to run Chrome
options = Options()
options.enable_downloads = True

# initialize a Chrome WebDriver instance
# with the specified options
driver = webdriver.Chrome(options=options)

# to avoid issues with responsive content
driver.maximize_window()


url = "https://wallpapers.99px.ru/wallpapers/tags/cyberpunk/"

wait = WebDriverWait(driver, 10)
driver.get(url)
image_html_node = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'photo2_tmb_img_o')))
driver.get(image_html_node.get_attribute("href"))


for _ in range(180):
  try:
    current_url = driver.current_url
    image_html_node = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="download_button"]')))
    driver.get(image_html_node.get_attribute("href"))
    time.sleep(5)
    image_url = wait.until(EC.presence_of_element_located((By.XPATH, '//a[text()="Сохранить файл"]')))
    image_url.click()
    # image_urls.append(image_url.get_attribute("href"))
    driver.get(current_url)
  except (StaleElementReferenceException, TimeoutException):
    continue
  finally:
    next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-hotkey="39"]')))
    driver.get(next_page.get_attribute("href"))



dest_path = r'C:\Users\sibag\Downloads'
source_path = r"D:\обои\Cyberpunk"
copy_dir = shutil.move(source_path, dest_path)


