# imports the required python libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sqlite3
from selenium.webdriver.chrome.options import Options

# create a sqlite with https://sqlitebrowser.org/dl/
options = Options()
# options.add_argument("window-size=1400,1000") which helps in having the browser at max size
options.add_argument("--start-maximized")
# city we are scraping data
city = "New York"
# state of the city we are scraping data
state = "NY"
# This is the base url for extracting information
base_url = "https://www.yelp.com/search?find_desc=Black%20Owned%20Restaurants&find_loc=" + city + "%2C%20" + state + "&start="

# Creates a bot with a browser driver. The bot helps automate data collection.
BotPath = "C:\workspace\chromedriver.exe"

# Creates a bot with a browser driver. The bot helps automate data collection.
bot = webdriver.Chrome(options=options, executable_path=BotPath)

# creating a connection object to represent the database
conn = sqlite3.connect('assets/bor.db')

# adds a cursor to the database
cursor = conn.cursor()

# bot gets the url which loads the web page
bot.get(base_url + str(0))

# Create a document object model (DOM) from the raw source of the crawled web page.
# Since we are processing a html page, 'html.parser' is chosen.
soup = BeautifulSoup(bot.page_source, 'html.parser')
time.sleep(5)

# keeps track of the page number where the data will be scraped from
pageNum = int(soup.find('div', class_='border-color--default__09f24__1eOdn text-align--center__09f24__1P1jK').text.split(" ")[2])

# loops through all the pages from yelp
for i in range(pageNum):
    if i != 0:
        time.sleep(5)
        # gets all the ten restaurants on the yelp website
        bot.get(base_url + str(i*10))
        soup = BeautifulSoup(bot.page_source, 'html.parser')
    # helps get the individual pages of restaurant name and adds it to the yelp website url
    restaurants = soup.find_all('div', class_='container__09f24__21w3G hoverable__09f24__2nTf3 margin-t3__09f24__5bM2Z margin-b3__09f24__1DQ9x padding-t3__09f24__-R_5x padding-r3__09f24__1pBFG padding-b3__09f24__1vW6j padding-l3__09f24__1yCJf border--top__09f24__8W8ca border--right__09f24__1u7Gt border--bottom__09f24__xdij8 border--left__09f24__rwKIa border-color--default__09f24__1eOdn')

    # This loops through the individual pages of restaurant and finds where a restaurant provides delivery and/or takeaway.
    # The data is then put into their respective lists
    for restaurant in restaurants:
        reviewNum = 0
        bReviewNum = 0
        name = ''
        feature = ''
        landline = ''
        stars = 0.0
        self_identified = 0
        gives_delivery = 0
        gives_takeout = 0

        # helps get the names of restaurants
        name = restaurant.find('a', class_='css-166la90').text
        # helps get the features of restaurants
        features = restaurant.find('p', class_='css-1j7sdmt').text
        # get the restaurants telephone contact when one exists on yelp
        if restaurant.find('p', class_='css-8jxw1i') != None:
            landline =  restaurant.find('p', class_='css-8jxw1i').text
        # get the restaurants address contact
        if restaurant.find('address') != None:
            address = restaurant.find('address').text
        else:
            try:
                address = restaurant.find('a', class_="css-ac8spe").text
            except:
                address = ""
        # reviews  css-n6i4z7      self-identified  css-8yg8ez

        # creates a boolean when a self identified black owned restaurant is found or reviewed black owned,
        # while scrapping yelp also keeps count of restaurants who are black owned identified or reviewed
        if restaurant.find("p", class_="css-n6i4z7") != None:
            self_identified = 0
            bReviewNum = int(restaurant.find("p", class_="css-n6i4z7").text.split(" ")[0])
        else:
            self_identified = 1
            bReviewNum = -1
        try:
            reviewNum = int(restaurant.find('span', class_='css-e81eai').text)
        except:
            pass

        # if rating of a restaurant is found, scraps the data
        try:
            stars = float(restaurant.find('div', class_='i-stars__09f24__1T6rz').attrs["aria-label"].split(" ")[0])
        except:
            pass

        # checks if a restaurant offers delivery service or not
        if restaurant.find("p", class_="css-192a8l5") != None:
            gives = restaurant.find("p", class_="css-192a8l5").text
            if "delivery" in gives:
                gives_delivery = 1
            if "takeout" in gives:
                gives_takeout = 1

        # posts the data collected into the sql database. Makes sure no restaurant is repeated
        insert_record_sql = "INSERT OR REPLACE INTO restaurants (name, address, city, state, features, reviewNum, bReviewNum, stars, identified, delivery, takeout) VALUES ('%s', '%s', '%s', '%s', '%s', %d, %d, %f, %d,%d,%d)" % (name, address, city, state, features, reviewNum, bReviewNum, stars, self_identified, gives_delivery, gives_takeout)
        print(str(i + 1), " of ", pageNum, ":", insert_record_sql)
        cursor.execute(insert_record_sql)
        conn.commit()

bot.close()
conn.close()
print ("finished.")
