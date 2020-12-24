import pandas as pd
from bs4 import BeautifulSoup
import requests


name_list=[]
img_list=[]
price_list=[]
size_list=[]
for r in range(1,14):
	page= requests.get('https://www.bitis.com.vn/collections/nam?page='+str(r))
	soup = BeautifulSoup(page.content, 'html.parser')
	name=soup.find_all("h3",class_="product_name")
	for j in name :
	 	name_list.append(j.getText().replace("*","").strip())
	img=soup.find_all("div",class_="product-image image-resize product-image-block")
	for i in img :
		img_list.append(i.find("img").get("src").strip())
	pri=soup.find_all("div",class_="product_prices m-t-10 m-b-10")
	for p in pri:
		price_list.append(p.find("span",class_="price").getText().replace("\n",'').strip())
data= {
		"name": name_list,
		"imglink": img_list,
		"price": price_list,
		
	}
df=pd.DataFrame(data)
df.to_excel('bitis.xlsx')
