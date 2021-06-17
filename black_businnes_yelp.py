# @author:          Aniruddh Vardhan
# @email:           aav5@uw.edu.
# date:             13th June,2021
# @description:     Search black-owned restaurants on yelp using a web crawler

from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime, json, csv
import grequests

base_url = "https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start="

bot = webdriver.Chrome(executable_path="assets/chromedriver.exe")

all_url = []
individual_restaurant_page = []

for i in range(0, 70, 10):
    new_url = base_url + str(i)
    all_url.append(all_url)

bot.get('https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start=0')

# Create a document object model (DOM) from the raw source of the crawled web page.
# Since you are processing a html page, 'html.parser' is chosen.
soup = BeautifulSoup(bot.page_source, 'html.parser')
time.sleep(5)
restaurants = soup.find_all('div', class_ = 'container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
yelp_website = 'https://www.yelp.com'
for restaurant in restaurants:
    restaurant_name = restaurant.find('a', class_='css-166la90').get('href')
    time.sleep(5)
    restaurant_page = yelp_website + str(restaurant_name)
    individual_restaurant_page.append(restaurant_page)

for information in individual_restaurant_page:
    bot.get(information)
    main_content_wrap = soup.find('div', class_ = 'main-content-wrap main-content-wrap--full')

    try:
        name = main_content_wrap.find('h1', class_='css-11q1g5y').text
        address = main_content_wrap.find('div', class_ = 'css-1vhakgw border--top__373c0__19Owr border-color--default__373c0__2oFDT').find_next('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-e81eai').text
        features = main_content_wrap.find('a', class_='css-166la90').text


row = {
    'name': name,
    'address': address,
    'feature': features
}

