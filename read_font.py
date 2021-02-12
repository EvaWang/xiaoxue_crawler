import time
from urllib.parse import urlparse, parse_qs, urlsplit
import argparse
import requests

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 

from crawler import *

# initiating the webdriver. Parameter includes the path of the webdriver. 
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_xiaozhuan_list(args, page):

    url = f"{args.root_url}/CCDB/PageResult/PageResult"
    payload= f'KaishuFreqCheck=false&KaishuFreqOrder=4000&FontCode=4&PaginalColNum=10&PaginalRowNum=5&ImageSize=5&PageTo={pageTo}'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    kaiOrder_set = set()

    soup = BeautifulSoup(response.text, "html.parser")
    char_list = soup.find_all('td', class_ = 'CharList')
    for char in char_list:
        kaiOrder_set.add(int(char.a.text))

    return  kaiOrder_set

def get_xiaozhuan_img(driver, args, folder_path, kaiOrder):

    url = args.target_url%(kaiOrder)
    
    driver.get(url)  
    time.sleep(3)

    html = driver.page_source 
    soup = BeautifulSoup(html, "html.parser")
    # TODO: 抓字型當作ground truth
    label_text = ""
    label = soup.find(id="EudcFontChar")
    if label:
        label_text = label.get("value", "")

    img_count = 0
    imgList = []

    char_variant_list = soup.find_all('img', class_ = 'charValue')
    for char_variant in char_variant_list:
        if char_variant.parent.get('class', None) is None:
            img_url = char_variant.get('src','')
            url_split = urlsplit(img_url)
            url_query_parse = url_split.query.split('&')
            url_query = [ param for param in url_query_parse if param.startswith('size=')==False]
            url_query.append("{}={}".format('size', args.size))

            save_from_url(args.root_url+url_split.path+"?"+"&".join(url_query), os.path.join(folder_path, "%s_%s.png"%(kaiOrder, img_count)))
            imgList.append({'img_id': img_count, 'desc': "楷書字型"})

            img_count = img_count+1

    char_list = soup.find_all('td', class_ = 'VariantListA')
    for char in char_list:
        img = char.img
        if img:
            img_url = img.get('src', None)
            url_split = urlsplit(img_url)
            url_query_parse = url_split.query.split('&')
            url_query = [ param for param in url_query_parse if param.startswith('size=')==False]
            url_query.append("{}={}".format('size', args.size))

            imgList.append({'img_id': img_count, 'desc': char.text})
            save_from_url(args.root_url+url_split.path+"?"+"&".join(url_query), os.path.join(folder_path, "%s_%s.png"%(kaiOrder, img_count)))

            img_count = img_count+1

    # json格式: {id: #kaiOrder, imgList:[{img_id: #img_id, desc: #出處}]
    return {'id': kaiOrder, 'charname': label_text, 'imgList': imgList}



def _parse_args():
    parser = argparse.ArgumentParser(
        description="爬蟲--小學堂網頁"
    )

    parser.add_argument('-f','--font', type=str, required=False, help='font', default='xiaozhuan')
    # parser.add_argument('-l','--limit', type=int, required=False, help='limit', default=11101)
    parser.add_argument('-s','--size', type=int, required=False, help='size', default=64)
    parser.add_argument('-p','--save_path', type=str, required=False, help='save_path', default='./')
    parser.add_argument('-r','--root_url', type=str, required=False, help='root_url', default='https://xiaoxue.iis.sinica.edu.tw')
    parser.add_argument('-u','--target_url', type=str, required=False, help='target_url', default='https://xiaoxue.iis.sinica.edu.tw/xiaozhuan?kaiOrder=%d')

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = _parse_args()
    print("Start crawlering...")
    print("Assume there are {} records.".format(args.limit))

    folder_path = os.path.join(args.save_path, args.font)
    create_folder(folder_path)
    driver = webdriver.Chrome(os.path.join(args.save_path, 'chromedriver'), options=chrome_options)  

    pageTo = 1
    while pageTo<500:
        kaiOrder_set = get_xiaozhuan_list(args, pageTo)
        if len(kaiOrder_set)==0:
            break
        pageTo = pageTo+1
        for char in kaiOrder_set:
            data = get_xiaozhuan_img(driver, args, folder_path, char)
            dump_jsonl(data, os.path.join(folder_path, 'xiaozhuan.jsonl'))

    driver.close() # closing the webdriver 
    print("Crawler done.")
    