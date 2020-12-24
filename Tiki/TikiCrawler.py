import pandas
from lxml import html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Define variables

categories = []
categories_link = []
items_link = []
items_name = []
items_current_price = []
items_list_price = []
items_discount_rate = []
items_brand = []

#Define functions

def hasXpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def hasFlashSale():
    if hasXpath("//div[@class='price-and-icon no-background']"):
        return True
    else:
        return False

def get_SalePrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__list-price']").text)
    items_current_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__current-price']").text)
    items_discount_rate.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__discount-rate']").text)

def get_NormalPrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__current-price']").text)
    items_discount_rate.append("None")
    items_current_price.append("None")

def get_FlashSalePrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='sale']//span[@class='list-price']").text)
    items_current_price.append(driver.find_element_by_xpath("//div[@class='flash-sale-price']//span").text)
    items_discount_rate.append(driver.find_element_by_xpath("//div[@class='sale']//span").text)

#Main function

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(chrome_options=options)

url = 'https://tiki.vn/' 
driver.get(url)

cate_link = driver.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']")
for i in cate_link:
    categories_link.append(i.get_attribute('href'))

categories_link.pop(10)
categories_link.append('https://tiki.vn/thoi-trang-nu/c931')
categories_link.append('https://tiki.vn/thoi-trang-nam/c915')

cate = driver.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']//span[@class='text']")
for i in cate:
    categories.append(i.text)

wait = WebDriverWait(driver, 10)

for i in range(0,2):
    driver.get(categories_link[i])
    wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//a[@class='product-item']")))
    
    item_in_cate = []

    items = driver.find_elements_by_xpath("//a[@class='product-item']")
    for j in items:
        item_in_cate.append(j.get_attribute('href'))
        items_link.append(j.get_attribute('href'))

    for link in item_in_cate:
        driver.get(link)
        wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='price-and-icon no-background'] | //div[@class='product-price']")))

        items_name.append(driver.find_element_by_xpath("//h1[@class='title']").text)

        if hasFlashSale():  
            get_FlashSalePrice()
        else:
            if hasXpath("//div[@class='product-price']//span[@class='product-price__list-price']"):
                get_SalePrice()
            else:
                get_NormalPrice()

        items_brand.append(driver.find_element_by_xpath("//h6//a").text)

driver.quit()

data = {
    "Product name" : items_name,
    "Product link" : items_link,    
    "Brand (Author)" : items_brand,
    "Original Price" : items_list_price,
    "Sale Price" : items_current_price,
    "Discount Rate" : items_discount_rate
}

df = pandas.DataFrame(data)
df.to_excel('Tiki.xlsx', index = False)