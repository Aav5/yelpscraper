# @author:          Aniruddh Vardhan
# @email:           aav5@uw.edu.
# date:             9th June,2021
# @description:     Search tweets of a specific topic using a web crawler

# imports the required python libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime, json

# The data will be collected from the url. The url comprises of information like including location, time period,
# keyword and hashtag
url = "https://twitter.com/search?l=&q=near%3A%22houston%22%20within%3A15mi%20since%3A" \
      "2017-08-24%20until%3A2017-08-31&src=typd&lang=en"

# Creates a bot with a browser driver. The bot helps automate data collection.
bot = webdriver.Chrome(executable_path="assets/chromedriver.exe")

# bot gets the url which loads the web page
bot.get(url)

# Declares the global variables and assigns initial values. Creates an empty csv file, writes a header to the csv
# file, and records the current time, stores all the collected tweets. Crawler runs for 60 minutes.
f = open("assets/tweets.csv", "a", encoding="utf-8") # create a csv file to store the collected tweets.
f.write('user_id, user_name, screen_name, status_id, created_at, time_integer, reply_num, retweet_num, favorite_num,content \n') # read the csv header
start = datetime.datetime.now()
time_limit = 60
texts = []

# Adds the scrolling ability. Sets time limit for the crawler and adds criterias to stop crawling. Also Processes only
# new acquired tweets.
while len(bot.find_elements_by_xpath('//div[contains(text(), "Back to top ↑")]')) != 1:
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html5lib')
    tweets = soup.find_all('li', class_="stream-item")[-20:]
    if int((datetime.datetime.now() - start).seconds) >= time_limit:
        break

# Tries to extract information from collected tweets about the author, the tweet, and identify whether it is a tweet
# synchronized from Instagram.
for tweet in tweets:
      try:
          user_json = json.loads(tweet.div.attrs["data-reply-to-users-json"])
          user_id = int(user_json[0]['id_str'])
          user_name = user_json[0]['screen_name']
          screen_name = user_json[0]['name']
          status_id = int(tweet.attrs["data-item-id"])
          text = tweet.find("p").text.strip().replace("\n", "")
          created_at = tweet.find("small", class_="time").a.attrs["title"]
          time_integer = tweet.find("small", class_="time").a.span["data-time-ms"]
          reply_num = tweet.find("div", class_="ProfileTweet-action--reply").find("span", class_="ProfileTweet-actionCountForPresentation").text
          retweet_num = tweet.find("div", class_="ProfileTweet-action--retweet").find("span", class_="ProfileTweet-actionCountForPresentation").text
          favorite_num = tweet.find("div", class_="ProfileTweet-action--favorite").find("span", class_="ProfileTweet-actionCountForPresentation").text
          inst_url = ""
          if "www.instagram.com" in text:
              inst_url = tweet.p.a.attrs["title"]
          ...
          ...
      except:
          pass

# Inserts the collected information to the csv file. Also checks if the information has been inserted previously and
# adds it to the csv file if not already existing.
for tweet in tweets:
      try:
          ...
          text = tweet.find("p").text.strip().replace("\n", "")
          ...
          record = '%d, %s, %s, %d, %s， %s， %s， %s， %s， %s \n' % (user_id, user_name, screen_name, status_id, created_at, time_integer, reply_num, retweet_num, favorite_num, text)
          print(record)
          if (text not in texts):
              f.write(record)
          texts.append(text)

# Closes both the csv file handler and the bot handler. and notifies that the data
# crawling task is done. If you execute this piece of python script on pyCharm, a file tweets.csv will be generated to
# the assets folder. 
f.close()
bot.close()
print("finished")
