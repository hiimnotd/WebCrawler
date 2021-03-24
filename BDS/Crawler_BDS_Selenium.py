import pandas as pd
import xlsxwriter
from lxml import html
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

	#declare variable 
link  = []
uid   = []
title = []
address = []
price = []        ###
des_product = []
phone = []		  ###
date  = []		  ###
area  = []        ###
image = []        ###
detail = []		  ###

	# At first I crawl all link of product in muaban page
def get_link_products():
	items = driver.find_elements_by_xpath("//a[@class='wrap-plink']")
	for j in items:
		link.append(j.get_attribute('href'))

	# Extract data description, title, address
def get_product_information():
	description = driver.find_elements_by_xpath("//div[@class='des-product']")
	for i in description:
		des_product.append(i.text)

	tit = driver.find_elements_by_xpath("//h1[@class='tile-product']")
	for j in tit:
		title.append(j.text)

	add = driver.find_elements_by_xpath("//div[@class='short-detail']")
	for i in add:
		address.append(i.text)

	# get price information
def get_price():
	price_product = driver.find_elements_by_xpath("//div[@class='short-detail-wrap']/ul/li[1]/span[2]")
	for i in price_product:
		price.append(i.text)
	# TO check does path exist or not?
def check_Xpath(xpath): 
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False
    #Get uid of product,
    # But the HTML structure be changed in some page so I have to check path first
def get_uid():
	if check_Xpath('//*[@id="product-detail-web"]/div[5]/div[8]/ul/li[4]/span[2]'):
		uid_product = driver.find_elements_by_xpath("//*[@id='product-detail-web']/div[5]/div[8]/ul/li[4]/span[2]")
	else:
		uid_product = driver.find_elements_by_xpath("//*[@id='product-detail-web']/div[5]/div[7]/ul/li[4]/span[2]")
	for i in uid_product:
		uid.append(i.text)
	
	#get date of product
	# Same way with get_uid() 
def get_date():
	if check_Xpath("//*[@id='product-detail-web']/div[5]/div[8]/ul/li[1]/span[2]"):
		date_product = driver.find_elements_by_xpath("//*[@id='product-detail-web']/div[5]/div[8]/ul/li[1]/span[2]")
	else:
		date_product = driver.find_elements_by_xpath("//*[@id='product-detail-web']/div[5]/div[7]/ul/li[1]/span[2]")
	for i in date_product:
		date.append(i.text)

	# get Area of product
	# But in some product there is no area information, Instead it is information about the bedroom,
def get_area():
	if check_Xpath("//div[@class='short-detail-wrap']/ul/li[2]/span[2]"):
		area_product = driver.find_elements_by_xpath("//div[@class='short-detail-wrap']/ul/li[2]/span[2]")
		for x in area_product:
			z = x.text
			if 'PN' in z:             # So I check word in string, if have 'PN' the area value = None
				area.append('None')
			else:
				area.append(z)
	else:
		area.append("None")

	# Get image of product, same problem with uid
def get_image():
	if check_Xpath("//div[@class='slide-product']/div/ul/li[1]/a"):
		image_product = driver.find_elements_by_xpath("//div[@class='slide-product']/div/ul/li[1]/a")
		for i in image_product:
			imag = i.get_attribute('style')
			if imag is not None:
				# Extract image link from a string, since image information be put in style prop so I have to extract a string to image's link 
				raw_img = re.search("(?P<url>https?://[^\s]+)", imag).group("url").strip('");')
				image.append(raw_img)
			else:
				image.append('None')
	else:
		image.append('None')

def get_phone_number():
	phone_number = driver.find_elements_by_xpath("/html/body/div[1]/div[7]/div[2]/div[7]/div/div[2]/div[4]")
	for i in phone_number:
		phone.append(i.get_attribute('raw'))

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:/Users/birus/Downloads/chromedriver_win32/chromedriver.exe")

for r in range(5):
	url = 'https://batdongsan.com.vn/nha-dat-ban/p'+ str(r)
	driver.get(url)
	get_link_products()

for i in link:
	driver.get(i)

	get_product_information()
	get_price()	
	get_phone_number()
	get_image()
	get_area()
	get_date()
	get_uid()

driver.quit()

data = {
	"UID": uid,
	"Title": title,
	"Address": address,
	"Price": price,
	"Area": area,
	"Image": image,
	"Description": des_product,
	"Link": link,
	"Phone": phone,
	"Date": date
}

#Export data to Excel
df = pd.DataFrame(data)
df.to_excel('whisss.xlsx')