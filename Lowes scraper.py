import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random


options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument('authority=www.lowes.com')
options.add_argument(
    'accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
options.add_argument('accept-language=en-US,en;q=0.9')
options.add_argument('cache-control=no-cache')
options.add_argument('pragma=no-cache')
options.add_argument('referer=https://www.lowes.com')
options.add_argument(
    'sec-ch-ua="Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"')
options.add_argument('sec-ch-ua-mobile=?0')
options.add_argument('sec-ch-ua-platform="Windows"')
options.add_argument('sec-fetch-dest=document')
options.add_argument('sec-fetch-mode=navigate')
options.add_argument('sec-fetch-site=same-origin')
options.add_argument('sec-fetch-user=?1')
options.add_argument('upgrade-insecure-requests=1')
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

driver.execute_script(
    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def mouse():
    delay = random.uniform(1, 3)
    time.sleep(delay)

    # Mouse movement
    webdriver.ActionChains(driver).move_by_offset(0, 0).perform()


def scrape_page_data(i):
    if i == 1:
        store = 90250
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'pl')))

        driver.execute_script("window.scrollBy(0, 2000);")
        input = driver.find_element(By.LINK_TEXT, 'Find My Store')
        webdriver.ActionChains(driver).click(input).perform()
        mouse()
        input = driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Zip Code, City, State or Store #']")
        webdriver.ActionChains(driver).click(input).perform()
        print('ffff')

        input = driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Zip Code, City, State or Store #']")
        webdriver.ActionChains(driver).send_keys_to_element(
            input, store).perform()

        mouse()
        webdriver.ActionChains(driver).send_keys_to_element(
            input, Keys.ENTER).perform()

        print('ssssss')

        mouse()
        # find the store number for the store you want. It's in the html on the button
        input = driver.find_element(
            By.CSS_SELECTOR, 'button[data-storenumber="1555"]')
        webdriver.ActionChains(driver).click(input).click().perform()

    # scroll down to load all content on the page
    mouse()
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 2000);")
        mouse()

    skus = driver.find_elements(By.CLASS_NAME, 'tooltip-custom')

    prices = driver.find_elements(By.CSS_SELECTOR, 'div.prdt-actl-pr')

    description = driver.find_elements(
        By.CSS_SELECTOR, '.titl-cnt.titl.brnd-desc')

    # you are scraping recommends that don't have this data
    return skus, prices, description


def pagination(url, pages=2):

    prod_num = []
    prod_price = []
    prod_desc = []

    page_num = 0
    # iterate over the pages
    for i in range(1, pages+1):

        # print(f"this is page {i}")
        driver.get(f"{url}?Nao={page_num}")
        skus, prices, description = scrape_page_data(i)

    for sku in skus:
        prod_num.append(sku.text)
    for price in prices:
        prod_price.append(price.text)
    for desc in description:
        prod_desc.append(desc.text)
    print(f"prod_num: {prod_num}")
    print(f"prod_price: {prod_price}")
    print(f"prod_desc: {prod_desc}")
    print(f"prod_num: {len(prod_num)}")
    print(f"prod_price: {len(prod_price)}")
    print(f"prod_desc: {len(prod_desc)}")

    # increment it by 24 since each page has 24 data
    page_num += 24
    mouse()

    return prod_num, prod_price, prod_desc


if __name__ == '__main__':
    website = 'https://www.lowes.com/pl/Drywall-panels-Drywall-Building-supplies/4294858283'
    # this section of code ads the URL paramater that adds a store. Just go and find the zip for the store you want to check pricing at. I used Hawthorne for example

    prod_num, prod_price, prod_desc = pagination(website, pages=1)

    # df = pd.DataFrame(
    #     {'code': prod_num, 'price': prod_price, 'brand': prod_desc})
    # df.to_csv('lowes.csv', index=False)
    # print(df)

    driver.quit()
