# Twitter-Scraping
A project to scrape tweets.

# Description:
This project is built to scrape data from Twitter using snscrape python package.

# Pre-requisites:
Snscrape
Streamlit
Pandas
Datetime
Pymongo
JSON

import streamlit as st
import snscrape.modules.twitter as tweetScraper
import pandas as pd
import datetime
import pymongo
import json as js

# UI:
The frontend is a simple and elegant single page user interface which displays a welcome message, gets some user inputs and has some buttons to perform few functions.

# Functions:
* The UI initially displays the welcome message.
"""
Twitter Scraping
Hello there, Welcome!
Let's scrape the data/tweets you want:
"""

* At the beginning, we connect to MongoDB.

* After the welcome message and connecting to DB, we have a button to clear previous records/tweets which will truncate the pre-existing records to give us only the records relating to our current search.

* A list to collect tweets is initiated.

* A slider to get the user input for number of tweets to be scraped is placed.

* Then user input is received on what type of item to be scraped. 'Keyword', 'Hashtag' or 'Username'.

* Start and end dates to scrape the tweets are received from the user.

* Search term is received from the user.

* Then the user inputs are collated and sent in as a single query inside snscrape.modules.Twitter.TwitterSearchScraper(query) function.

* The script starts to scrape the data and time is taken according to the number of tweets requested by the user.

* Scraped tweets and their details are store in the previously initiated list and then converted into a pandas dataframe.

* This data is inserted into MongoDB.

* Then two buttons are given to download the data.

* One "Download data as CSV" button and one "Download data as JSON" button.

* "Download data as CSV" converts the df into CSV format and downloads it.

* "Download data as JSON" converts the df into JSON format and downloads it.

* Finally the tweets and raw data are displayed which can also be used to preview the data before downloading.
