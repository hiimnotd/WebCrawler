import requests
import bs4
import pandas

all_link = []
names = []
prices = []
imgs = []
all_img = []
infors = []
all_infor = []

#Get all link
for i in range (1,5):
   page = requests.get("https://www.hanoicomputer.vn/tan-nhiet-cooling/" + str(i) + "/")
   soup = bs4.BeautifulSoup(page.content, "html.parser")

   attribute = soup.find_all("div", {"class": "p-component item"})
   for j in attribute:
      link = j.find("a")
      all_link.append("https://www.hanoicomputer.vn" + link.get("href"))


#Crawl data from each link
for i in all_link:
   page = requests.get(i)
   soup = bs4.BeautifulSoup(page.content,"html.parser")

   names.append(soup.find("div",{"class":"product_detail-title"}).text.replace("\n","").strip())

   prices.append(soup.find("b", {"id": "p-info-price"}).text.replace("\n", "").strip())

   img_temp = soup.find_all("li", {"class": "owl-thumb-item"})
   for j in img_temp:
      img = j.find("img")
      imgs.append(img.get("src"))
   if imgs == []:
      imgs = "Not Given"
   all_img.append(imgs)
   imgs = []

   try:
      info_temp = soup.find("div", {"class": "bang-tskt"})
      detail = info_temp.find_all("td")
      for i in detail:
         infors.append(i.find("p").text.replace("\n", "").strip())
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

# print("\n".join(all_link))
# print(len(all_link))
# print("\n".join(names))
# print("\n".join(prices))
# for j in all_img:
#    for k in j:
#       print(k, sep=' ')
# for j in all_infor:
#    for k in j:
#       print(k, sep=' ')
# print(len(all_img))
# print(len(all_infor))

data = {
   "Name": names,
   "Link": all_link,
   "Price": prices,
   "Image": all_img,
   "Information": all_infor
}
df = pandas.DataFrame(data)
df.to_csv(r'PC.csv', index = False)