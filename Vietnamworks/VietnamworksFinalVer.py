#Import the packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import  ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
import array as arr
import pandas


#Define 
all_link = []
content = []
name_job = []
name_company = []
name_location = []
salary = []
all_salary = []
expiry = []
upload_date = []
position = []
career = []
skill = []
language_of_cv = []
detail_address = []
number_employees = []
all_link_del_duplicates = []
notice = 'Information is missed'


#Chrome Options
option = webdriver.ChromeOptions()
CDM = ChromeDriverManager()
chrome_options = Options()
chrome_options.add_argument ('--ignore-certificate-errors')
chrome_options.add_argument ("--igcognito")
chrome_options.add_argument ("--window-size=1920x1080")
chrome_options.add_argument ('--headless')


#Set path for webdriver
driver = webdriver.Chrome(CDM.install(),chrome_options=chrome_options,options=option)


#Open log-in url
driver.get("https://secure.vietnamworks.com/login/vi?client_id=3") 
driver.maximize_window()


#Time-wait
time.sleep(10)


#Fill the log-in information
driver.find_element_by_id("email").send_keys("luongdg.bi9159@st.usth.edu.vn") #PUT YOUR EMAIL HERE
driver.find_element_by_id('login__password').send_keys('Conanpro123')         #PUT YOUR PASSWORD HERE
driver.find_element_by_id("button-login").click()


#Crawl all the links of job
url = 'https://www.vietnamworks.com/tim-viec-lam/tat-ca-viec-lam'
driver.get(url)
time.sleep(10)

page_num = 1
driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

while page_num <= 40:
    #crawl all the link and the salary in each page
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,"html.parser")
    block_job_list = soup.find_all("div",{"class":"block-job-list"})
    for i in block_job_list:
        link_catalogue = i.find_all("div",{"class":"col-12 col-lg-8 col-xl-8 p-0 wrap-new"})
        for j in link_catalogue:
            link = j.find("a")
            all_link.append("https://www.vietnamworks.com" + link.get("href"))
        salary_catalogue = i.find_all("div",{"class":"col-12 col-lg-4 col-xl-4 p-0 col-salary"})
        for j in salary_catalogue:
            salary = j.find("span")
            all_salary.append(salary.text.replace("\n","").strip())

    # moves to next page
    try:
        print(f'On page {str(page_num)}')
        print()
        page_num+=1
        driver.find_element_by_link_text(str(page_num)).click()
        time.sleep(3)

    # checks only at the end of the page
    except NoSuchElementException:
        print('End of pages')
        break

driver.quit()

#Remove all duplicates links
[all_link_del_duplicates.append(x) for x in all_link if x not in all_link_del_duplicates]

print("\n".join(all_link_del_duplicates))
print(len(all_link_del_duplicates))


#Enter to every links to crawl the data
for i in all_link_del_duplicates:
    page = requests.get(i)
    soup = BeautifulSoup(page.content,"html.parser")
    name_job.append(soup.find("h1",{"class":"job-title"}).text.replace("\n","").strip())

    name_company.append(soup.find("div",{"class","company-name"}).text.replace("\n","").strip())

    name_location.append(soup.find("span",{"class":"company-location"}).text.replace("\n","").strip())

    information = soup.find_all("div",{"class":"row summary-item"})
    for i in information:
        content.append(i.find("span",{"class":"content"}).text.replace('\xa0','').replace('\n', '').replace('  ',"").strip())

    try:
        upload_date.append(content[0])
    except IndexError:
        upload_date.append(notice)

    try:
        position.append(content[1])
    except IndexError:
        position.append(notice)

    try:
        career.append(content[2])
    except IndexError:
        career.append(notice)

    try:
        skill.append(content[3])
    except IndexError:
        skill.append(notice)

    try:
        language_of_cv.append(content[4])
    except IndexError:
        language_of_cv.append(notice)

    try:
        detail_address.append(content[5])
    except IndexError:
        detail_address.append(notice)

    try:
        number_employees.append(content[6])
    except IndexError:
        number_employees.append(notice)

    content =[]

data = {
   "Name": name_job,
   "Salary": all_salary,
   "Upload date": upload_date,
   "Locations": name_location,
   "Skill": skill,
   "Career": career,
   "Company": name_company,
   "Job position": position,
   "Number employees": number_employees,
   "Detail address": detail_address,
   "Language of cv": language_of_cv,
   "Link job" : all_link,
}

df = pandas.DataFrame(data)
df.to_excel(r'Vietnamworks2.xlsx', index = False)
