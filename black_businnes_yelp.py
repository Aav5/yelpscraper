# @author:          Aniruddh Vardhan
# @email:           aav5@uw.edu.
# date:             13th June,2021
# @description:     Search black-owned restaurants on yelp using a web crawler

# imports the required python libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime, json, csv

# This is the base url for extracting information
base_url = "https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start="

# Creates a bot with a browser driver. The bot helps automate data collection.
bot = webdriver.Chrome(executable_path="assets/chromedriver.exe")

# stores all the urls of different pages
all_url = []

# holds information of different individual restaurant pages, it is used to get extract information about specific restaurant
individual_restaurant_page = []

# holds the names of the restaurants
names = []

# holds the address of the restaurants
addresses = []

# holds the features of the restaurants
features = []

# holds the number of reviews of the restaurants
reviews = []

# holds the star rating of the restaurants
stars = []

# loops through different pages, which helps generate different urls
for i in range(0, 70, 10):
    new_url = base_url + str(i)
    all_url.append(all_url)

# bot gets the url which loads the web page
bot.get('https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start=0')

# Create a document object model (DOM) from the raw source of the crawled web page.
# Since you are processing a html page, 'html.parser' is chosen.
soup = BeautifulSoup(bot.page_source, 'html.parser')
time.sleep(5)

# helps get the individual pages of restaurant name and adds it to the yelp website url
restaurants = soup.find_all('div', class_='container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
yelp_website = 'https://www.yelp.com'
for restaurant in restaurants:
    restaurant_name = restaurant.find('a', class_='css-166la90').get('href')
    time.sleep(5)
    restaurant_page = yelp_website + str(restaurant_name)
    individual_restaurant_page.append(restaurant_page)

# helps gets the information of particular restaurant pages
for information in individual_restaurant_page:
    bot.get(information)
    # gets the main content box where all the restaurants information exists
    main_content_wrap = soup.find('div', class_='main-content-wrap main-content-wrap--full')

    try:
        # extracts the name of the restaurant and adds it into all restaurant name list
        name = main_content_wrap.find('h1', class_='css-11q1g5y').text
        names.append(name)
        # extracts the address of the restaurant and adds it into all restaurant address list
        address = main_content_wrap.find('div', class_='css-1vhakgw border--top__373c0__19Owr border-color--default__373c0__2oFDT').find_next('p', class_ = 'css-1h1j0y3').find_next('p', class_ = 'css-e81eai').text
        addresses.append(address)
        # extracts the feature of the restaurant and adds it into all restaurant features list after making it into a string
        feature = main_content_wrap.find('a', class_='css-166la90').text
        stringify_feature = str(feature)
        features.append(stringify_feature)
        # extracts the total reviews of the restaurant and adds it into all restaurant reviews list
        review = main_content_wrap.find('span', class_='css-bq71j2').text
        reviews.append(review)
        # extracts the star rating of the restaurant and adds it into all restaurant star rating
        star = main_content_wrap.find('div', class_="i-stars__373c0__1T6rz i-stars--large-4-half__373c0__2lYkD border-color--default__373c0__30oMI overflow--hidden__373c0__2B0kz").text
        stars.append(star)

    except:
        pass

# create a row in the dict format.
row = {
    'name': names,
    'address': addresses,
    'feature': features,
    'reviews': reviews,
    'stars': stars
}

