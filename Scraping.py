#Importing required packages
import streamlit as st
import snscrape.modules.twitter as tweetScraper
import pandas as pd
import datetime
import pymongo
import json as js

#Displaying a welcome message
"""
# Twitter Scraping
Hello there, Welcome!
Let's scrape the data/tweets you want:
"""

def tweetscrape():
    #Connecting to MongoDB
    client = pymongo.MongoClient("mongodb+srv://mahdoom:1234@cluster0.rbr6oyu.mongodb.net/?retryWrites=true&w=majority")
    db = client.Twitter_Scrape
    record = db.Scraped_data

    #Setting up a button to clear previous records/tweets
    clear = record.delete_many({})
    st.button("Click to clear previous records", clear)

    #Setting up a list to collect tweets
    tweets_list = []

    #Setting up a slider to get the user input for number of tweets to be scraped
    num = st.slider('Number of tweets', 10, 1000, step = 10)
    st.write('You selected:', num)

    #Getting user input on what type of item to scrape
    item = st.selectbox('How do you want to search by? Using:', ['Keyword', 'Hashtag', 'Username'])
    st.write('You have selected', item)
    items = ['Keyword', 'Hashtag', 'Username']

    #Getting user input for date range for the tweets to be scraped
    d = st.date_input('Please select the start date:', datetime.date(2023, 1, 1))
    st.write('Tweets since: ', d)

    d1 = st.date_input('Please select the end date:', datetime.date(2023, 3, 1))
    st.write('Tweets until: ', d1)

    #Main code block goes here
    #Getting the search term from the user and scraping the tweets using snscrape module
    if item in items:
        search_term = st.text_input('Enter the search term: ')
        date_range = ' since:'+d.strftime("%Y-%m-%d")+' until:'+d1.strftime("%Y-%m-%d")
        query = search_term+date_range
        #st.write(query)
        scraper = tweetScraper.TwitterSearchScraper(query)
        #st.write('You entered:', scraper)
        for i, tweet in enumerate(scraper.get_items()):
            if i > (num - 1):
                break
            tweets_list.append([
                i + 1, tweet.date, tweet.id, tweet.url, tweet.rawContent, tweet.user.username, tweet.replyCount,
                tweet.retweetCount, tweet.lang, tweet.source, tweet.likeCount
            ])
    #Converting the data to a pandas dataframe
    df = pd.DataFrame(tweets_list,
                      columns=["No.", "Date", 'ID', 'URL', 'Tweet(s)', 'Username', 'Reply count', 'Retweet count',
                               'Language', "Source", "Likes count"])

    #Inserting data into the DB
    tweet_data = js.loads(df.to_json(orient='records'))
    record.insert_many(list(tweet_data))

    #dftweets = pd.DataFrame(list(record.find()))

    #Converting data to csv and json to download
    @st.cache_data
    def convert_df_to_csv(df):
       return df.to_csv().encode('utf-8')

    csv = convert_df_to_csv(df)
    st.download_button(
       "Download data as CSV",
       csv,
       "file.csv",
       "text/csv",
        key='download-csv'
    )

    def convert_df_to_json(df):
       return df.to_json().encode('utf-8')

    json = convert_df_to_json(df)
    st.download_button(
       "Download data as JSON",
       json,
       "file.json",
       "text/json",
       key='download-json'
    )

    #st.dataframe(df)

    #Displaying the tweets
    st.write('Tweets:')
    st.write(df['Tweet(s)'])
    # Displaying the raw data which has date, id, url, tweet, retweet and like counts, etc.,
    st.write('Raw Data:')
    st.write(df)

tweetscrape()