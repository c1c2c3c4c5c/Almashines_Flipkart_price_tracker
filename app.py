from flask import Flask, render_template, request
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

app = Flask(__name__)

def scrape_flipkart(product_name):
    flipkart_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
    response = requests.get(flipkart_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find("div", {"class": "_30jeq3"}).text.strip()
    return f'Flipkart: {price}'

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from selenium import webdriver



def scrape_amazon(product_name):
    amazon_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)

    driver.get(amazon_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    price_element = soup.select_one(".a-price .a-offscreen")
    if price_element:
        price = price_element.text.strip()
        driver.quit()  
        return f'Amazon: {price}'
    else:
        driver.quit() 
        return 'Amazon: Price not found'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        if product_name:
            flipkart_price = scrape_flipkart(product_name)
            amazon_price = scrape_amazon(product_name)
            return render_template('index.html', flipkart_price=flipkart_price, amazon_price=amazon_price)
    return render_template('index.html', flipkart_price=None, amazon_price=None)

if __name__ == '__main__':
    app.run(debug=True)
