# https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/

from nltk.tokenize import word_tokenize
import re
import json

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(word_tokenize(tweet))
# ['RT', '@', 'marcobonzanini', ':', 'just', 'an', 'example', '!', ':', 'D', 'http', ':', '//example.com', '#', 'NLP']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
print(preprocess(tweet))

# PREPROCESS all tweets
# Further improvements regular expression to capture more data, or using Named Entity Recognition.
with open('mytweets.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        tokens = preprocess(tweet['text'])
        # do_something_else(tokens)


# Counting Words
import operator
import json
from collections import Counter

fname = 'mytweets.json'
with open(fname, 'r') as f:
  count_all = Counter()
  for line in f:
      tweet = json.loads(line)
      # Create a list with all the terms
      terms_all = [term for term in preprocess(tweet['text'])]
      # Update the counter
      count_all.update(terms_all)
  # Print the first 5 most frequent words
  print(count_all.most_common(5))

# Removing STOP WORDS

# from nltk.corpus import stopwords
# import string

# punctuation = list(string.punctuation)
# stop = stopwords.words('english') + punctuation + ['rt', 'via']
# terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
# Count terms only once, equivalent to Document Frequency
#terms_single = set(terms_all)
# Count hashtags only
#terms_hash = [term for term in preprocess(tweet['text'])
#              if term.startswith('#')]
# Count terms only (no hashtags, no mentions)
#terms_only = [term for term in preprocess(tweet['text'])
#              if term not in stop and
#              not term.startswith(('#', '@'))]
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if
              # we pass a list of inputs

from nltk import bigrams

terms_bigram = bigrams(terms_stop)

