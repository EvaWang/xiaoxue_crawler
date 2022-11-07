import time
from urllib.parse import urlparse, parse_qs, urlsplit
import argparse

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 

from crawler import *

# initiating the webdriver. Parameter includes the path of the webdriver. 
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_xiaozhuan_list_url(driver, args, folder_path, ZiOrder):

    url = args.target_url%(ZiOrder)
    print(url)
    
    driver.get(url)  
    time.sleep(5)  
    

    next_page = True
    img_count = 0
    imgList = []

    while next_page:

        html = driver.page_source 
        soup = BeautifulSoup(html, "html.parser")
    
        # TODO: 抓字型當作ground truth
        label_text = ""
        label = soup.find(id="ZiOrder")
        if label:
            label_text = label.get("value", "")

        char_variant_list = soup.find_all('img', class_ = 'charValue')
        for char_variant in char_variant_list:
            if char_variant.parent.get('class', None) is None:
                img_url = char_variant.get('src','')
                url_split = urlsplit(img_url)
                url_query_parse = url_split.query.split('&')
                url_query = [ param for param in url_query_parse if param.startswith('size=')==False]
                url_query.append("{}={}".format('size', args.size))

                #save_from_url(args.root_url+url_split.path+"?"+"&".join(url_query), os.path.join(folder_path, "%s_%s.png"%(ZiOrder, img_count)))
                imgList.append({'img_id': img_count, 'desc': "字頭", "img_url":args.root_url+url_split.path+"?"+"&".join(url_query)})

                img_count = img_count+1

        char_list = soup.find_all('td', class_ = 'VariantListA')
        char_list = char_list + soup.find_all('td', class_ = 'VariantListB')
        for char in char_list:
            img = char.img
            if img:
                img_url = img.get('src', None)
                url_split = urlsplit(img_url)
                url_query_parse = url_split.query.split('&')
                url_query = [ param for param in url_query_parse if param.startswith('size=')==False]
                url_query.append("{}={}".format('size', args.size))

                #save_from_url(args.root_url+url_split.path+"?"+"&".join(url_query), os.path.join(folder_path, "%s_%s.png"%(ZiOrder, img_count)))
                imgList.append({'img_id': img_count, 'desc': char.text, "img_url": args.root_url+url_split.path+"?"+"&".join(url_query)})
                img_count = img_count+1

        pager= None
        try:
            pager = driver.find_element(By.LINK_TEXT, '下一頁')
            pager.click()
            time.sleep(5)  
        except:
            print('next page not found.')
            next_page = False

    # json格式: {id: #ZiOrder, imgList:[{img_id: #img_id, desc: #出處}]
    return {'id': ZiOrder, 'charname': label_text, 'imgList': imgList}



def _parse_args():
    parser = argparse.ArgumentParser(
        description="爬蟲--小學堂網頁"
    )

    parser.add_argument('-f','--font', type=str, required=False, help='font', default='jiaguwen')
    parser.add_argument('-l','--limit', type=int, required=False, help='limit', default=3956)
    parser.add_argument('-s','--size', type=int, required=False, help='size', default=64)
    parser.add_argument('-p','--save_path', type=str, required=False, help='save_path', default='./')
    parser.add_argument('-r','--root_url', type=str, required=False, help='root_url', default='https://xiaoxue.iis.sinica.edu.tw')
    parser.add_argument('-u','--target_url', type=str, required=False, help='target_url', default='https://xiaoxue.iis.sinica.edu.tw/jiaguwen?ZiOrder=%d')
    parser.add_argument('--start_idx', type=int, required=False, help='target_url', default=1)

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = _parse_args()
    print("Start crawlering...")
    print("Assume there are {} records.".format(args.limit))

    folder_path = os.path.join(args.save_path, args.font)
    create_folder(folder_path)
    
    retry = 3
    driver = webdriver.Chrome(os.path.join(args.save_path, 'chromedriver'), chrome_options=chrome_options)  
    for i in range(args.start_idx, args.limit+1):
        while retry>0:
            try:
                data = get_xiaozhuan_list_url(driver, args, folder_path, i)
                dump_jsonl(data, os.path.join(folder_path, 'jiaguwen.jsonl'))
                retry = 3
                break
            except:
                print(f"retry {retry} times")
                time.sleep(5)
                retry = retry-1
        

    driver.close() # closing the webdriver 
    print("Crawler done.")
