import requests
import bs4
import pandas
import time
import concurrent.futures

categories_link = []
all_link = []
names = []
prices = []
all_img = []
all_infor = []
product_link = []

get_request = time.time()

page = requests.get("https://www.hanoicomputer.vn/")
soup = bs4.BeautifulSoup(page.content,"html.parser")
classes = soup.find_all("li",{"class":"js-hover-menu"})
for i in classes:
   link_class = i.find("a")
   categories_link.append("https://www.hanoicomputer.vn" + link_class.get("href"))

#Delete duplicate link
del categories_link[18:]

print("\n".join(categories_link))
print(len(categories_link))

for i in categories_link:
   for j in range(1,4):
      page = requests.get(i+"/"+str(j)+"/")
      soup = bs4.BeautifulSoup(page.content, "html.parser")

      attribute = soup.find_all("div", {"class": "p-component item"})
      for j in attribute:
         link = j.find("a")
         all_link.append("https://www.hanoicomputer.vn" + link.get("href"))

   # print("\n".join(all_link))
   # print(len(all_link))
while 'https://www.hanoicomputer.vn/cable-mini-display-port-to-display-port-1.8m.' in all_link:
   all_link.remove('https://www.hanoicomputer.vn/cable-mini-display-port-to-display-port-1.8m.')
while 'https://www.hanoicomputer.vn/pin-cmos' in all_link:
   all_link.remove('https://www.hanoicomputer.vn/pin-cmos')
while 'https://www.hanoicomputer.vn/khay-dat-hddssd-caddy-35-cho-laptop-va-desktop-orico-1106ss' in all_link:
   all_link.remove('https://www.hanoicomputer.vn/khay-dat-hddssd-caddy-35-cho-laptop-va-desktop-orico-1106ss')
del all_link[2100:]
request_end = time.time()
print(f'Request runtime is: {request_end-get_request}')

dat = {
   "Link" : all_link,
}
df = pandas.DataFrame(dat)
df.to_csv(r'link.csv', index=False)

start_crawl = time.time()
def crawl_product(url):
   infors = []
   imgs = []
   page = requests.get(url)
   soup = bs4.BeautifulSoup(page.content, "html.parser")

   product_link.append(url)

   try:
      names.append(soup.find("div", {"class": "product_detail-title"}).text.replace("\n", "").strip())
      #print("\n".join(names))
   except AttributeError:
      print("name error")
      print(url)

   try:
      prices.append(soup.find("b", {"id": "p-info-price"}).text.replace("\n", "").strip())
   except AttributeError:
      print("price error")
      print(url)
      prices.append(soup.find("span", {"class": "status-products"}).text.replace("\n", "").strip())

   img_temp = soup.find_all("li", {"class": "owl-thumb-item"})
   for j in img_temp:
      img = j.find("img")
      imgs.append(img.get("src"))
   if imgs == []:
      div = soup.find("div", {"class": "img-item"})
      img = div.find("img")
      imgs.append(img.get("src"))
   all_img.append(imgs)
   imgs = []

   try:
      info_temp = soup.find("div", {"class": "bang-tskt"})
      detail = info_temp.find_all("td")
      for i in detail:
         infors.append(i.find_all("p").text.replace("\n", "").strip())
      infors = ["Not Given" if x == '' else x for x in infors]
      if infors == []:
         infors = "Not Given"
      all_infor.append(infors)
      infors = []
   except AttributeError:
      info_temp = soup.find("div", {"class": "bang-tskt"})
      detail = info_temp.find_all("td")
      for i in detail:
         infors.append(i.text.replace("\n", "").strip())
      infors = ["Not Given" if x == '' else x for x in infors]
      if infors == []:
         infors = "Not Given"
      all_infor.append(infors)
      infors = []
   return

with concurrent.futures.ThreadPoolExecutor() as run:
   run.map(crawl_product, all_link)

end_crawl = time.time()
print(f'Crawling runtime is: {end_crawl-start_crawl}')

print(len(names))
print(len(product_link))
print(len(prices))
print(len(all_img))
print(len(all_infor))
# print("\n".join(product_link))

data = {
   "Name": names,
   "Link": product_link,
   "Price": prices,
   "Image": all_img,
   "Information": all_infor,
}
df = pandas.DataFrame(data)
df.to_excel('hanoicomputer.xlsx', index= False)
df.to_csv(r'hanoicomputer.csv', index=False)