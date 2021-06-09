import re, requests
from flask import Flask, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)
CORS(app)

# GET /stores
@app.route('/stores')
def get_stores():
# extracting name of store and code from #url
    url = "#url"
    get_url = requests.get(url)
    soup = BeautifulSoup(get_url.text, 'html.parser')
    headings = soup.findAll('h4')

    all_shop_data = []

    #getting all the tags inside each h4 
    for tag in headings:
        # extracting all the contents of anchor tag
        for name in tag.findAll('a'):
            store_name = name.text 
            store_code = name.get('href')
            # extracting only numbers from href
            store_code = re.sub('[^0-9]','', store_code)
            # converting string into int
            store_code_int = int(store_code)
            # arranging the data to show output as json
            shop_data = {"store": store_name, "store_number": store_code_int)}
            all_shop_data.append(shop_data)
    return jsonify({'stores': all_shop_data})


# Configure host and port
if __name__ == '__main__':
    app.run(port=5000)




