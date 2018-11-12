# https://stats.seandolinar.com/collecting-twitter-data-converting-twitter-json-to-csv-possible-errors/

import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import io

ckey = 'WwC84Up9EWsDaFTQdKQolWHTX'
consumer_secret = 'RtMSxqdGW4wCpFJCXHzFhbsowYbv8FFiIQGVyQ3cMwxh5mcXSx'
access_token_key = '44842866-94tb5tG7r4INSftcirVHOtcxVyVPdtJ7rhdqoXrfq'
access_token_secret = 'LD3jUJas86QtPqZnc4lsIPJbIDy5sOw8C3w8uE57060UF'

start_time = time.time() #grabs the system time
keyword_list = ['twitter'] #track list
from pymongo import MongoClient
import json

class listener(StreamListener):
  def __init__(self, start_time, time_limit=60):
    self.time = start_time
    self.limit = time_limit

  def on_data(self, data):
    while (time.time() - self.time) < self.limit:
      try:
        client = MongoClient('localhost', 27017)
        db = client['twitter_db']
        collection = db['twitter_collection']
        tweet = json.loads(data)
        collection.insert(tweet)
        return True
      except Exception as e:
        print('failed ondata,', str(e))
        time.sleep(5)
      pass
    exit()

  def on_error(self, status):
    print(status)

  def getTweets(self):
    try:
      client = MongoClient('localhost', 27017)
      db = client['twitter_db']
      collection = db['twitter_collection']

      # text = tweet['text']
      # user_screen_name = tweet['user']['screen_name']
      # user_name = tweet['user']['name']
      # retweet_count = tweet['retweeted_status']['retweet_count']
      # retweeted_name = tweet['retweeted_status']['user']['name']
      # retweeted_screen_name = tweet['retweeted_status']['user']['screen_name']
      # collection.find({'text' : 'This will return tweets with only this exact string.'})
      # tweets = collection.find({'user.screen_name' : 'exactScreenName'})
      # tweets = collection.find({'text': { '$regex' : 'word'}})
      # collection.find({"retweeted_status" : { "$exists" : "true"}})

      tweets_iterator = collection.find()
      for tweet in tweets_iterator:
          print(tweet['text'])
      return True
    except Exception as e:
      print('failed get tweets,', str(e))
      time.sleep(5)
    pass

auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)

twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object

