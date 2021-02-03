import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

#Define variables

category_list = []
category_link = []
name_list = []
item_link = []
item_category = []
current_price = []
list_price = []
sale_rate = []
size_list = []

#Crawl Data

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(chrome_options=options)

url = 'https://www.bitis.com.vn'
page= requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

category = soup.find_all("li", class_="has_child")
category.append(soup.find_all("h2",class_="title")[2])
for i in range(1,len(category)):
	category_link.append(category[i].find("a").get("href"))
	category_list.append(category[i]t.find("a").getText().upper())

for cate in category_link:
	for i in range(1,18):
		final_url = url+cate+"?page="+str(i)
		driver.get(final_url)
		page = requests.get(final_url)
		soup = BeautifulSoup(page.content, 'html.parser')

		if soup.find('div', class_='product-lists-item'):
			elements = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.product-lists-item")))
			for element in elements:
				size_of_item = []

				ActionChains(driver).move_to_element(element).perform()
				sizes = element.find_elements_by_css_selector('span.size_item')
				for s in sizes:
					size_of_item.append(s.text)
				
				if (size_of_item[0] != ""):
					size_list.append(size_of_item)
				else:
					size_list.append("None")

			name = soup.find_all("h3",class_="product_name")
			for j in name :
				name_list.append(j.getText().replace("*","").strip())
				item_category.append(category_list[category_link.index(cate)])

			link = soup.find_all("div",class_="product-image image-resize product-image-block")
			for l in link:
				item_link.append(url + l.find("a").get("href"))	
				
			pri = soup.find_all("div",class_="product_prices m-t-10 m-b-10")
			for p in pri:
				current_price.append(p.find("span",class_="price").getText())
				if p.find('span', class_='saleoff'):
					list_price.append(p.find("del").getText())
					sale_rate.append(p.find("span", class_="saleoff").getText())
				else:
					list_price.append("None")
					sale_rate.append("None")
		else:
			break

driver.quit()

data= {	
		"Name": name_list,
		"Product Link": item_link,
		"Category": item_category,
		"Size": size_list,
		"Current Price": current_price,
		"Original Price": list_price,
		"Sale Rate": sale_rate
	}
df=pd.DataFrame(data)
df.to_excel('bitis.xlsx', index = False)