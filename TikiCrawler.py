from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

categories = []
categories_link = []
items_link = []

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(chrome_options=options)

url = 'https://tiki.vn/' 
driver.get(url)

cate_link = driver.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']")
for i in cate_link:
    categories_link.append(i.get_attribute('href'))

categories_link.pop(10)

cate = driver.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']//span[@class='text']")
for i in cate:
    categories.append(i.text)

wait = WebDriverWait(driver, 10)

for i in categories_link:
    driver.get(i)
    wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//a[@class='product-item']")))
    
    items = driver.find_elements_by_xpath("//a[@class='product-item']")
    for j in items:
        items_link.append(j.get_attribute('href'))

    for link in items_link:
        driver.get(link)
        wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='product-price']")))
        
        list_price = driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__list-price']").text
        current_price = driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__current-price']").text
        discount_rate = driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__discount-rate']").text
        brand = driver.find_element_by_xpath("//h6//a[@data-view-id='pdp_details_view_brand']").text

        print(list_price)
        print(current_price)
        print(discount_rate)
        print(brand)

driver.quit()
