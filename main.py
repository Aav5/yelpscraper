

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
# @author:          Aniruddh Vardhan
# @email:           aav5@uw.edu.
# date:             13th June,2021
# @description:     Search black-owned restaurants on yelp using a web crawler

# imports the required python libraries
from selenium import webdriver
from bs4 import BeautifulSoup
from pathlib import Path
import time
import csv
import sqlite3
import pandas as pd

# This is the base url for extracting information
base_url = "https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start="

# Creates a bot with a browser driver. The bot helps automate data collection.
# bot = webdriver.Chrome(executable_path="assets/chromedriver")

BotPath = "C:\workspace\chromedriver.exe"
# bot = webdriver.Chrome(executable_path="assets/chromedriver.exe")
bot = webdriver.Chrome(executable_path=BotPath)

# Create a csv file to store the structured data after processing.
csvfile = open("assets/black_restaurant_data.csv", "w", newline='', encoding="utf-8")

# All the fields of each data entry that I want to collect.
# added get_black_owned to test what exactly what data is being collect
fieldnames = ['name', 'address', 'feature', 'reviews', 'stars', 'self-identified', 'delivery', 'takeaway', 'get_black_owned']

# Create a writer to write the structured data to the csv file.
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

# Write the header to the csv file
writer.writeheader()

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

# will hold whether a restaurant is self_identified black owned by owners or reviewers
self_identified = []

# will store whether all the restaurant deliver or not
delivery = []

# will store whether all the restaurant gives takeaway or not
takeaway = []

# for test purpose, this would hold exactly what data is getting collected
black_owned = []

# loops through different pages, which helps generate different urls
# for i in range(0, 70, 10):
#     new_url = all_url + str(i)
#     all_url.append(all_url)

# bot gets the url which loads the web page
bot.get('https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start=0')

# Create a document object model (DOM) from the raw source of the crawled web page.
# Since we are processing a html page, 'html.parser' is chosen.
soup = BeautifulSoup(bot.page_source, 'html.parser')
time.sleep(8)

# helps get the individual pages of restaurant name and adds it to the yelp website url
restaurants = soup.find_all('div', class_='container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
yelp_website = 'https://www.yelp.com'
for restaurant in restaurants:
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    restaurant_name = restaurant.find('a', class_='css-166la90').get('href')
    time.sleep(8)
    restaurant_page = yelp_website + str(restaurant_name)
    individual_restaurant_page.append(restaurant_page)

# this should work but isnt I tried explaining this in the previous email on july 6th
# these code lines intend to check what data is being collected. My expected data which would be stored would be Black-owned but it is not giving the expected output
    try:
        get_black_owned = restaurant.find('span', class_=' raw__09f24__3Obuy').get_text()
        black_owned.append(get_black_owned)
        # if get_black_owned == "Black-owned":
        #     self_identified_restaurant = 1
        # else:
        #     self_identified_restaurant = 0
        # self_identified.append(self_identified_restaurant)
    except AttributeError:
        get_black_owned = 'none'
        black_owned.append(get_black_owned)

# helps gets the information of particular restaurant pages
for information in individual_restaurant_page:
    bot.get(information)
    # gets the main content box where all the restaurants information exists
    time.sleep(8)
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    main_content_wrap = soup.find('div', class_='main-content-wrap main-content-wrap--full')

    try:
        # extracts the name of the restaurant and adds it into all restaurant name list
        name = main_content_wrap.find('h1', class_='css-11q1g5y').get_text()
        names.append(name)
    except AttributeError:
        name = 'NULL'
        names.append(name)
    try:
        # extracts the address of the restaurant and adds it into all restaurant address list
        address = main_content_wrap.find('p', class_ = 'css-chtywg').get_text()
        addresses.append(address)
    except AttributeError:
        address = 'NULL'
        addresses.append(address)
    except TypeError:
        address = 'Null'
        addresses.append(address)

    try:
        # extracts the feature of the restaurant and adds it into all restaurant features list after making it into a string
        feature = main_content_wrap.find('a', class_='css-166la90').get_text()
        stringify_feature = str(feature)
        features.append(stringify_feature)
        more_feature = main_content_wrap.find_all('span', class_='css-166la90').get_text()
        more_stringify_feature = str(more_feature)
        features.append(more_stringify_feature)
    except AttributeError:
        pass
    try:
        # extracts the total reviews of the restaurant and adds it into all restaurant reviews list
        review = main_content_wrap.find('span', class_='css-bq71j2').get_text()
        reviews.append(review)
    except AttributeError:
        review = 'NONE'
        reviews.append(review)
    #     # extracts the star rating of the restaurant and adds it into all restaurant star rating
    try:
        # star = main_content_wrap.find('div', class_=' i-stars__373c0__1T6rz')['aria-label']
        star = main_content_wrap.find('div', class_=' i-stars__373c0__1T6rz').get('aria-label')
        print(star)
        stars.append(star)
    except AttributeError:
        star = 'None'
        stars.append(star)

# commented below lines as they were showing errors. Partly correct

# This loops through the individual pages of restaurant and finds where a restaurant provides delivery and/or takeaway.
# The data is then put into their respective lists
# for restaurant in restaurants:
#     check_mark = soup.find('span', class_='icon--24-checkmark-v2 css-yyirv3')
#     cross_mark = soup.find('span', class_='icon--24-close-v2 css-p5yz4n')
#     delivery_takeaway_wrap = soup.find('div', class_=' display--inline-block__373c0__2de_K margin-r3__373c0__r37sx margin-b1__373c0__1khoT border-color--default__373c0__2oFDTl')
#     delivery_mark = soup.find('span', class_=' css-1h1j0y3')
#     takeaway_mark = soup.find('span', class_=' css-1h1j0y')
#     if delivery_mark in delivery_takeaway_wrap:
#         if check_mark in delivery_takeaway_wrap:
#             gives_delivery = 1
#         else:
#             gives_delivery = 0
#     delivery.append(gives_delivery)
#     if takeaway_mark in delivery_takeaway_wrap:
#         if check_mark in delivery_takeaway_wrap:
#             gives_takeaway = 1
#         else:
#             gives_takeaway = 0
#     takeaway.append(gives_takeaway)

# Below is code when I was trying different ways to collect data about self-identified "black-owned" restaurants.
# Similar code is used around line 96

# word = 'Black-owned'
# soup = BeautifulSoup(bot.page_source, 'html.parser')
# first_page_containers = soup.find_all('div', class_=' arrange-unit__09f24__3IxLD arrange-unit-fill__09f24__1v_h4 border-color--default__09f24__1eOdn')
# first_page_containers = soup.find_all('div', class_='container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
# for boxes in first_page_containers:
#     try:
#         get_black_owned = boxes.find('span', class_=' raw__09f24__3Obuy').get_text()
#         black_owned.append(get_black_owned)
#     except AttributeError:
#         get_black_owned = 'null'
#         black_owned.append(get_black_owned)
    # if get_black_owned == word:
    #     self_identified_restaurant = 1
    # else:
    #     self_identified_restaurant = 0
    # self_identified.append(self_identified_restaurant)
    # bot.get(boxes)
    # try:
    #     get_black_owned = boxes.findall('span', class_=' raw__09f24__3Obuy').get_text()
    #     if get_black_owned == word:
    #         self_identified_restaurant = 1
    #     else:
    #         self_identified_restaurant = 0
    #     self_identified.append(self_identified_restaurant)
    # except TypeError:
    #     self_identified_restaurant = 2
    #     self_identified.append(self_identified_restaurant)
    # except AttributeError:
    #     self_identified_restaurant = 2
    #     self_identified.append(self_identified_restaurant)

# some more attempts to extract self-identifies black-owned restaurants

# test_url = "https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=seattle%2C%20wa&start=0"
# for pages in test_url:
#     print(pages)
#     time.sleep(8)
#     soup = BeautifulSoup(bot.page_source, 'html.parser')
#     main_page_wrap = soup.all_find('div', class_=' container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')
#     for blocks in main_page_wrap:
#         print(blocks)
#         try:
#             bot.get(blocks)
#             soup = BeautifulSoup(bot.page_source, 'html.parser')
#             list_of_restaurant = soup.find_all('span', class_=' raw__09f24__3Obuy').get_text()
#             print(list_of_restaurant)
#     # string_list_of_restaurant = str(list_of_restaurant)
#     # if word in list_of_restaurant:
#             if list_of_restaurant == 'Black-owned':
#                 self_identified_restaurant = 1
#             else:
#                 self_identified_restaurant = 0
#             self_identified.append(self_identified_restaurant)
#         except TypeError:
#             self_identified_restaurant = 2
#             self_identified.append(self_identified_restaurant)
#         except AttributeError:
#             self_identified_restaurant = 2
#             self_identified.append(self_identified_restaurant)

# create a row in the dict format.
row = {
    'name': names,
    'address': addresses,
    'feature': features,
    'reviews': reviews,
    'stars': stars,
    'self-identified': self_identified,
    'delivery': delivery,
    'takeaway': takeaway,
    'get_black_owned': black_owned
}

# the restaurant information would be inserted.
print(row)
writer.writerow(row)

# # Let the bot scrolls down to the bottom of the content element, most of the time the bot needs to scroll down to the
# # bottom of the page like this statement: bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# bot.execute_script('window.scrollTo(0,  document.getElementById("content").scrollHeight);')
#
# # closes the csv file and the bot object.
# csvfile.close()
# bot.close()

# Haven't played with this code yet as wanted to get a correct csv dataset

# Create a database connection and cursor to execute queries.
# Path('black_restaurant_data.db').touch()
# connect = sqlite3.connect('black_restaurant_data.db')
# connection = connect.cursor()
#
# # Executes a query that will create a table with required columns.
# connection.execute('''CREATE TABLE users (name text,address text,reviews int,stars int, self-identified int,
#  delivery int, takeaway int)''')
#
# # loads the data into a Pandas DataFrame
# black_restaurant_data = pd.read_csv('black_restaurant_data.csv')
#
# # writes the data to a sqlite table
# black_restaurant_data.to_sql('black_restaurant_data', connect, if_exists='append', index=False)
# connection.execute('''SELECT * FROM black_restaurant_data''').fetchall()
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
