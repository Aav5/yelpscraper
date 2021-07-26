# Scrapping black owned restaurant from yelp's server

In this research project, I have practiced scrapping data from yelp website
about black owned restaurants using python web crawler. The projects gets useful
information about restaurants like restaurant name, address, city, state,
features, rating (stars), landline (if any), number of reviews,
blacked reviewed restaurants, and whether restaurants are self-identified
black-owned restaurants or not and lastly, whether they provide delivery or
takeout services

# Using the Script to collect data/ Running the code

To use the script makes sure to add the python libraries before running the code. The libraries used
in the project were Selenium, BeautifulSoup4, Time, Sqlite3

#  Customize the input parameter to enable crawler data from different cities

To change the input parameter to scrape data about different just change the city and state variable
in the code to extract the desired cities data

In the current program city name is "New York" and the state is "NY". Which extracts
data about black owned restaurants in New York city

# Collecting data from LGBTQ+ friendly restaurants

The current script is not supporting to collect data about LGBTQ+ data.
However, if the goal for your project is extracting data about LGBTQ+ friendly restaurants,
you must change the code accordingly.

# Why we need a 5-second pause?

If given a close look at the code, you might have realized there is a 5-second pause
at several locals. This is done so avoid the yelp server to be overloaded ( by too many requests)
in a very short period of time. Without using the pause, yelp website would realize 
that data is being scraped using a bot and thus could lead to a ban by yelp for your IP address.

# Finding css class from website used in the code

The css class is extremely important when scrapping data from a website. The css class
helps in communicating your computer about the location where the data is to be
extracted from in the webpage.


# Viewing the data extracted

The script is programmed to store data in sqlite3 format. To view this data you should have
DB Browser for SQLite. An example of how your output would look like is shown below.


![Image of Exacted Data](https://github.com/Aav5/yelpscraper/blob/main/assets/Output.png)

### Special thanks to Bo Zhao
