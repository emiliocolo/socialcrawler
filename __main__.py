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

class listener(StreamListener):
  def __init__(self, start_time, time_limit=60):
    self.time = start_time
    self.limit = time_limit
    self.tweet_data = []

  def on_data(self, data):
    saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')
    while (time.time() - self.time) < self.limit:
      try:
        self.tweet_data.append(data)
        return True

      except Exception as e:
        print('failed ondata,', str(e))
        time.sleep(5)
      pass

    saveFile = io.open('raw_tweets.json', 'w', encoding='utf-8')
    saveFile.write(u'[\n')
    saveFile.write(','.join(self.tweet_data))
    print(self.tweet_data)
    saveFile.write(u'\n]')
    saveFile.close()

    exit()

  def on_error(self, status):
    print(status)

auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)

twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object

