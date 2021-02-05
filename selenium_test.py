import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
import time 
  
#url of the page we want to scrape 
url = "https://www.naukri.com/top-jobs-by-designations# desigtop600"
xiaozhuan_url = "https://xiaoxue.iis.sinica.edu.tw/xiaozhuan?kaiOrder=59"
  
# initiating the webdriver. Parameter includes the path of the webdriver. 
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/nfs/home/evawang/font_crawler/chromedriver', chrome_options=chrome_options)  
# driver = webdriver.Chrome('/nfs/home/evawang/font_crawler/chromedriver')
driver.get(xiaozhuan_url)  
  
# this is just to ensure that the page is loaded 
time.sleep(5)  
  
html = driver.page_source 
  
# this renders the JS code and stores all 
# of the information in static HTML code. 
  
# Now, we could simply apply bs4 to html variable 
soup = BeautifulSoup(html, "html.parser") 
char_list = soup.find_all('td', class_ = 'VariantListA')
for char in char_list:
    # img = char.get('img', None)
    img = char.img
    if img:
        print(img.get('src', None))
  
# printing top ten job profiles 
# count = 0
# for job_profile in job_profiles : 
#     print(job_profile.text) 
#     count = count + 1
#     if(count == 10) : 
#         break
  
driver.close() # closing the webdriver 