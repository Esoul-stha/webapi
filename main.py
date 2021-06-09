from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from requests_html import HTMLSession
from bs4 import BeautifulSoup 
import requests
import os
from dotenv import load_dotenv
import re

app = Flask(__name__)
CORS(app)

# 店舗名と店舗コードに関わるコード
 load_dotenv()

 home_url = os.environ['URL']

 session = HTMLSession()


 with open('allshopdata.json','w') as jsonfile:
     get_url = session.get(home_url)

     get_url.html.render(sleep=1)

     kyushu = get_url.html.xpath('//*[@id="######"]', first=True)

     all_shop_data = []


     for all_kyushu_store in kyushu.absolute_links:
         get_store = requests.get(all_kyushu_store)
         soup = BeautifulSoup(get_store.text, 'html.parser')
         all_kyushu_store = soup.findAll('div', attrs = {'class':'shop_list'})
        
         for shop_list in all_kyushu_store:
             link = shop_list.findAll('h4')

             for shop_name in link:
                 links = shop_name.findAll('a')
                 for name in links:
                     store_name = name.text
                     store_code = name.get('href')
                     store_code = re.sub('[^0-9]','', store_code)
                     store_code_int = int(store_code)
                     shop_data = {"store": store_name, "store_number": '{0:04d}'.format(store_code_int)}
                     all_shop_data.append(shop_data)
     json.dump(all_shop_data, jsonfile, indent=4, ensure_ascii=False)
              
 all_stores = all_shop_data



# GET /stores
@app.route('/stores')
def get_stores():
    return jsonify({'stores': all_stores})



# ホーム画面にhtmlを読み込んでみる。
# GET /
@app.route('/')
def home():
    return render_template("index.html")

app.run(port=5000)




