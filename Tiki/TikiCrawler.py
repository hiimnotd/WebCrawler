from bs4 import BeautifulSoup
import pandas
import xlsxwriter
from lxml import html
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Define variables

categories = []
categories_link = []
items_link = []
items_name = []
items_category = []
items_current_price = []
items_list_price = []
items_discount_rate = []
items_brand = []
items_sku = []
items_detail = []
items_option = []
items_guarantee = []

#Define functions

#Check if Xpath exist or not
def hasXpath(xpath): 
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

#Check for Flash sale
def hasFlashSale(): 
    if hasXpath("//div[@class='flash-sale-price']"):
        return True
    else:
        return False

#Get price if product has sale
def get_SalePrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__list-price']").text)
    items_current_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__current-price']").text)
    items_discount_rate.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__discount-rate']").text)

#Get price if product has no sale
def get_NormalPrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='product-price']//span[@class='product-price__current-price']").text)
    items_discount_rate.append("None")
    items_current_price.append("None")

#Get price if product has flash sale
def get_FlashSalePrice():
    items_list_price.append(driver.find_element_by_xpath("//div[@class='sale']//span[@class='list-price']").text)
    items_current_price.append(driver.find_element_by_xpath("//div[@class='flash-sale-price']//span").text)
    items_discount_rate.append(driver.find_element_by_xpath("//div[@class='sale']//span").text)

#Get brand or author of product, if no brand is provided then return None
def get_Brand():
    if hasXpath("//h6//a"):
        items_brand.append(driver.find_element_by_xpath("//h6//a").text)
    else:
        items_brand.append("None")
    
#Get link of product
def get_item_links():
    wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//a[@class='product-item']")))

    items = driver.find_elements_by_xpath("//a[@class='product-item']")
    for j in items:
        item_in_cate.append(j.get_attribute('href'))

#Return options like color, capacity... of product
def get_Options():
    if hasXpath("//p[@class='option-name']"):
        op = []
        optional = driver.find_elements_by_xpath("//p[@class='option-name']//span")

        for o in optional:
            op.append(o.text)
    
        items_option.append(op)
    else:
        items_option.append("None")

#Return guarantee time of product, if no guarantee then return None
def get_guarantee():
    if hasXpath("//div[@class='warranty-item']//span[@class='itemRight']"):
        guarantee = driver.find_element_by_xpath("//div[@class='warranty-item']//span[@class='itemRight']").text
        items_guarantee.append(guarantee)
    else:
        items_guarantee.append("None")

#Get detailed information of product
def get_details():
    check_sku = False
    prop = []
    if hasXpath("//tbody"):
        table = driver.find_element_by_xpath("//tbody")
        rows = table.find_elements_by_xpath(".//tr//td")

        for cell in range(0, len(rows), 2):
            prop.append(rows[cell].text + ": " + rows[cell+1].text)

            if (rows[cell].text == "SKU"):
               items_sku.append(rows[cell+1].text)
               check_sku = True
        
        if (check_sku == False):
            items_sku.append("None") 

        items_detail.append(prop)
    else:
        items_detail.append("None")
        items_sku.append("None")
        

#Main function

#Set options for web driver
#Include: Headless, disable gpu, and set web driver to fullscreen size (with my computer it's 1920x1080)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(chrome_options=options)

#Request to homepage of tiki
url = 'https://tiki.vn/' 
driver.get(url)

#Get link to each category of tiki
#Becasue we need to hover main menu in order to get each category link
#So I used an ActionChains move_to_element in Selenium to perform like a real user
element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@class='Menu-button']")))
ActionChains(driver).move_to_element(element).perform()
cate_link = element.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']")
for i in cate_link:
    categories_link.append(i.get_attribute('href'))

#Tiki responsed an empty link in Fashion category
#So I need to implement them manually
categories_link.pop(10)
categories_link.append('https://tiki.vn/thoi-trang-nu/c931')
categories_link.append('https://tiki.vn/thoi-trang-nam/c915')

#Get category name to export
#It is same to getting categories link, I also need to implement categories's names manually
cate = driver.find_elements_by_xpath("//a[@data-view-id='main_navigation_item']//span[@class='text']")
for i in cate:
    categories.append(i.text)
categories.pop(10)
categories.append("Thời Trang Nữ")
categories.append("Thời Trang Nam")

#Create a WebDriverWait (maximum 10 seconds)
wait = WebDriverWait(driver, 10)

for i in categories_link:
    #Request to each category
    driver.get(i)
    #Get product link to request
    #Sometimes, DOM operation happening on the page is temporarily causing the element to be inaccessible.
    #So if this Exception throwed, I let the WebDriver refresh
    try:  
        item_in_cate = []
        get_item_links()
    except StaleElementReferenceException:
        driver.refresh()
        item_in_cate = []
        get_item_links()

    for j in item_in_cate:
        items_link.append(j)

    for link in item_in_cate:
        #Set category of each item to export
        items_category.append(categories[categories_link.index(i)])

        #Request to link of each product
        driver.get(link)

        #If I request to Tiki's server to much, it will block me from accessing to Tiki
        #The solution is that I refresh WebDriver again
        #Need an Explicit Wait for price elements located
        #Also need an Implicitly Wait (about 0.5s) for all elements that i need from webpage to load
        try:
            wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//span[@class='list-price'] | //span[@class='product-price__current-price']")))
            driver.implicitly_wait(0.5)
        except TimeoutException:
            driver.refresh()
            wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//span[@class='list-price'] | //span[@class='product-price__current-price']")))
            driver.implicitly_wait(0.5)

        #Get products's names
        items_name.append(driver.find_element_by_xpath("//h1[@class='title']").text)

        #Check if the product has Flash sale, Sale or not
        #Get price in each case by using functions were defined
        if hasFlashSale():  
            get_FlashSalePrice()
        else: 
            if hasXpath("//div[@class='product-price']//span[@class='product-price__list-price']"):
                get_SalePrice()
            else:
                get_NormalPrice()

        #Get Brand(or Author), Options, Guarantee time and Detailed information of product
        get_Brand()
        get_Options()
        get_guarantee()
        get_details()
        
#Turn off WebDriver after finishing scarb
driver.quit()

#Use DataFrame function to add each array to be a column in exported Excel file
data = {
    "Product name" : items_name,
    "Category": items_category,
    "Product link" : items_link,    
    "Brand (Author)" : items_brand,
    "Original Price" : items_list_price,
    "Sale Price" : items_current_price,
    "Discount Rate" : items_discount_rate,
    "Options" : items_option,
    "Guarantee" : items_guarantee,
    "SKU": items_sku,
    "Details" : items_detail
}

df = pandas.DataFrame(data)

writer = pandas.ExcelWriter('Tiki.xlsx', engine='xlsxwriter')

#Write data to Sheet1 of excel file
df.to_excel(writer, sheet_name='Sheet1', index=False)       

workbook = writer.book
worksheet = writer.sheets['Sheet1']

#Find largest length of each column to fill all data
for i, col in enumerate(df.columns):
    column_len = df[col].astype(str).str.len().max()
    column_len = max(column_len, len(col))
    worksheet.set_column(i, i, column_len)
writer.save()