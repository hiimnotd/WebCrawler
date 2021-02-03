import requests
import bs4
import pandas

categories_link = []
all_link = []
names = []
prices = []
imgs = []
all_img = []
infors = []
all_infor = []

page = requests.get("https://www.hanoicomputer.vn/")
soup = bs4.BeautifulSoup(page.content,"html.parser")

classes = soup.find_all("li",{"class":"js-hover-menu"})
for i in classes:
   link_class = i.find("a")
   categories_link.append("https://www.hanoicomputer.vn" + link_class.get("href"))

#Delete duplicate link
del categories_link[18:]

# print("\n".join(categories_link))
# print(len(categories_link))

for i in categories_link:
   for j in range(1,3):
      page = requests.get(i+"/"+str(j)+"/")
      soup = bs4.BeautifulSoup(page.content, "html.parser")

      attribute = soup.find_all("div", {"class": "p-component item"})
      for j in attribute:
         link = j.find("a")
         all_link.append("https://www.hanoicomputer.vn" + link.get("href"))

   # print("\n".join(all_link))
   # print(len(all_link))

#Crawl data from each link
for i in all_link:
   page = requests.get(i)
   soup = bs4.BeautifulSoup(page.content,"html.parser")

   try:
      names.append(soup.find("div", {"class": "product_detail-title"}).text.replace("\n", "").strip())
   except AttributeError:
      print("error")
      print(i)

   try:
      prices.append(soup.find("b", {"id": "p-info-price"}).text.replace("\n", "").strip())
   except AttributeError:
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

data = {
   "Name": names,
   "Link": all_link,
   "Price": prices,
   "Image": all_img,
   "Information": all_infor
}
df = pandas.DataFrame(data)
df.to_csv(r'hanoicomputer.csv', index = False)