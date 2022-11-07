import time
import argparse
import os
from crawler import load_jsonl, create_folder
import subprocess


def _parse_args():
    parser = argparse.ArgumentParser(
        description="爬蟲--小學堂網頁"
    )

    parser.add_argument('--save_path', type=str, required=False, help='save_path', default='./font_crawler/jiaguwen')
    parser.add_argument('--file_list', type=str, required=False, help='file_list', default='./font_crawler/jiaguwen/jiaguwen3.jsonl')

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = _parse_args()
    print("Start crawlering...")

    folder_path = os.path.join(args.save_path, "img")
    create_folder(folder_path)
    char_list = load_jsonl(args.file_list)

    for char in char_list:
        img_list = char["imgList"]
        id = char["id"]
        print(id)
        
        for img in img_list: 
            if img["desc"] != '字頭':
                print(img["img_url"])
                # print(f"-O {folder_path}/{id}_{img['img_id']}.png")
                subprocess.run(["wget", "-O", f"{folder_path}/{id}_{img['img_id']}.png", img["img_url"]])
                # subprocess.run(["wget", f"-O {folder_path}/{id}_{img['img_id']}.png", img["img_url"]])
                time.sleep(3)

    print("Crawler done.")
    
