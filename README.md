# 小學堂 漢字古今字資料庫 爬蟲
https://xiaoxue.iis.sinica.edu.tw/ccdb

## 拆解url
以小篆資料庫為例：

https://xiaoxue.iis.sinica.edu.tw/xiaozhuan?kaiOrder=1

- root url: https://xiaoxue.iis.sinica.edu.tw
- root之後的第一個segment `xiaozhuan` 表示為小篆資料庫，其他資料庫以此類推
- 參數`kaiOrder`代表字號，小篆從1開始編，推測有9831個字（參考網頁說明：本資料庫共收錄小篆字頭9831個，字形11101個。）

## 爬蟲參數
- font: 字型, ex: xiaozhuan
- limit: 收錄字數
- size: 圖片大小(pixel)
- save_path: 存檔路徑的root folder
- root_url: 小學堂資料庫網頁的root，抓圖會用到
- target_url: 目標資料庫網址，ex: https://xiaoxue.iis.sinica.edu.tw/xiaozhuan?kaiOrder=%d。 `kaiOrder`參數填入`%d`，讓程式碼可以動態塞入參數。

## 資料格式
- 程式會依照`font`參數建立資料夾，以小篆為例:
    ```
    .
    └── xiaozhuan 
        ├── [ 657]  998_0.png
        ├── [1.0K]  998_1.png
        ├── [ 976]  999_1.png
        └── [150K]  xiaozhuan.jsonl
    ```
    - 圖檔名稱格式: `{kaiOrder}_{img order}.png`
    - 資料夾內會有一個以font為檔名的jsonl檔案，儲存圖片描述，
    - 圖面描述: 以`xiaozhuan.jsonl`為例，若有一個以上楷書字型代表有異體字，其餘描述為出處。
        ```
        {
            "id": 886, 
            "charname": "怖", 
            "imgList": [
                {"img_id": 0, "desc": "楷書字型"},
                {"img_id": 1, "desc": "楷書字型"}, 
                {"img_id": 2, "desc": "說文‧心部"}, 
                {"img_id": 3, "desc": "說文或體"}
            ]
        }
        ```
        ![image](./readme_img/886_0.png)
        ![image](./readme_img/886_1.png)
        ![image](./readme_img/886_2.png)
        ![image](./readme_img/886_3.png)
        

## requirement

pip install selenium

