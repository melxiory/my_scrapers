import time
from pprint import pprint
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# initialize a Chrome WerbDriver instance
driver = webdriver.Chrome()

# to avoid issues with responsive content
driver.maximize_window()

# the URL of the target page
url = "https://unsplash.com/s/photos/wallpaper?license=free"
# visit the target page in the controlled browser
wait = WebDriverWait(driver, 10)
driver.get(url)
button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Load more"]')))
button.click()
time.sleep(1)
# select the node images on the page
image_html_nodes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid=\"non-sponsored-photo-download-button\"]")))

# where to store the scraped image url
image_urls = []
for image_html_node in image_html_nodes:
  try:
    image_url =  image_html_node.get_attribute("href")
    image_urls.append(image_url)
  except StaleElementReferenceException as e:
    continue

image_name_counter = 1
# download each image and add it
# to the "/images" local folder
for image_url in image_urls:
  print(f"downloading image no. {image_name_counter} ...")
  file_name = f"./images/{image_name_counter}.jpg"
  # download the image
  urllib.request.urlretrieve(image_url, file_name)
  print(f"images downloaded successfully to \"{file_name}\"\n")
  image_name_counter += 1

driver.quit()

