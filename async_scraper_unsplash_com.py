import time
import os
import shutil
import asyncio
import aiohttp
import aiofiles
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scraping(driver, wait):
  # изначально на странице 20 фото, после нажатия 40 фото
  button = wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Load more"]')))
  button.click()
  time.sleep(1)
  # каждый цикл увеличивает количество фото на 20
  for _ in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
  # ищем все кнопки для скачивания оригинального изображения
  image_html_nodes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid=\"non-sponsored-photo-download-button\"]")))
  image_urls = []
  # вытаскиваем URL для скачивания
  for image_html_node in image_html_nodes:
    try:
      image_url = image_html_node.get_attribute("href")
      image_urls.append(image_url)
    except StaleElementReferenceException:
      continue
  return image_urls

async def download_pictures(image_url, number, session, semaphore):
  async with semaphore:
    async with session.get(image_url) as resp:
      if resp.status == 200:
        async with aiofiles.open(f"./images/{number}.png", "wb") as f:
          print(f"downloading image no.{number} ...")
          await f.write(await resp.read())
          print(f"images downloaded successfully to \"./images/{number}.png\"\n")


async def main():
  # Инициализация драйвера Хрома
  driver = webdriver.Chrome()
  driver.maximize_window()
  # URL для скрапинга, можно подставить и другой "https://unsplash.com/s/photos/nature?license=free"
  # главное чтобы структура сайта не менялась
  url = "https://unsplash.com/s/photos/desktop-wallpapers?license=free"
  # устанавливаем таймаут для ожидания загрузки html объектов
  wait = WebDriverWait(driver, 10)
  driver.get(url)
  image_urls = scraping(driver, wait)
  # удаление и создание пустой папки
  shutil.rmtree('./images', ignore_errors=True)
  os.mkdir('images')
  # устанавливаем семафор чтобы не перегружать сервер
  semaphore = asyncio.Semaphore(5)
  # запускаем сессию и задачу на скачивание на каждый URL
  async with aiohttp.ClientSession() as session:
    downloaders = [asyncio.create_task(download_pictures(image_url, number, session, semaphore)) for number, image_url in enumerate(image_urls)]
    await asyncio.gather(*downloaders)
  driver.quit()


if __name__ == '__main__':
  curr_time = time.time()
  asyncio.run(main(), debug=True)
  print(f'Total time: {round(time.time() - curr_time, 2)}s')