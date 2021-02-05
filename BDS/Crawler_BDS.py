import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import re

	#declare array for data
link  = []
uid   = []
title = []
address = []
price = []
des_product = []
phone = []
date  = []
area  = []
image = []
detail = []

	# Make a request to homepage and take all link of products
for r in range(100):
	page= requests.get('https://batdongsan.com.vn/nha-dat-ban/p' + str(r))
	soup = BeautifulSoup(page.content, 'html.parser')
	print(page.status_code)
	wrap_link = soup.find("div", class_= "product-lists").find_all("div", class_= "product-item")
	for i in wrap_link:
		link.append("https://batdongsan.com.vn" + i.find("a").get("href"))
		uid.append(i.get("uid"))

	#Make request to each of all product to crawl data 
for k in link:
	page= requests.get(k)
	print(page.status_code)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Extract information
	description = soup.find("div", class_ = "description")
	short_detail = description.find("div", class_="short-detail-wrap").find("ul").find_all("li")
	short_detail_2 = description.find('div', class_='detail-product').find('div', class_='product-config').find('ul').find_all('li')
	imag = soup.find('li', class_='swiper-slide').find('a').get('style')

	# Add information to container
	title.append(description.find("h1").text.strip())
	address.append(description.find("div", class_="short-detail").text.strip())
	date.append(short_detail_2[0].find('span', class_= "sp3").text)
	price.append(short_detail[0].find("span", class_ = "sp2").text)
	des_product.append(description.find("div", class_= 'des-product').text.strip())
	phone.append(soup.find("div", class_="phone").find('span').get("raw"))
	 
	# check if product has no image then append None value
	if imag is not None:
		# Extract image link from a string 
		raw_img = re.search("(?P<url>https?://[^\s]+)", imag).group("url").strip("')")
		image.append(raw_img)
	else:
		image.append('None')

	# Check if product has no area information append None value
	try:
		area.append(short_detail[1].find('span', class_ = "sp2").text)
	except IndexError:
		area.append('None')

data = {
	"UID": uid,
	"Title": title,
	"Address": address,
	"Price": price,
	"Area": area,
	"Image": image
	"Description": des_product,
	"Link": link,
	"Phone": phone,
	"Date": date
}

#Export data to Excel
df = pd.DataFrame(data)
df.to_excel('t.xlsx')