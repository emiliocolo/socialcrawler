import json
from nltk.tokenize import word_tokenize
import re

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

# with open('./data/stream_microsoft.json', 'r') as f:
#    line = f.readline() # read only the first tweet/line
#    tweet = json.loads(line) # load it as Python dict
#    print(json.dumps(tweet, indent=4)) # pretty-print

# pre process all tweets
# with open('./data/stream_microsoft.json', 'r') as f:
#    for line in f:
#        tweet = json.loads(line)
#        tokens = preprocess(tweet['text'])
#        print(tokens)

# Term frequencies
import operator
from collections import Counter
from collections import defaultdict
from nltk.corpus import stopwords
from nltk import bigrams
import string

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', 'de', 'en']

fname = './data/stream_microsoft.json'
with open(fname, 'r') as f:
  count_all = Counter()
  for line in f:
    tweet = json.loads(line)
    # Create a list with all the terms
    terms_all = [term for term in preprocess(tweet['text'])]
    # Create a list with all the terms without stop words
    terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
    # Count terms only once, equivalent to Document Frequency
    terms_single = set(terms_all)
    # Count hashtags only
    terms_hash = [term for term in preprocess(tweet['text'])
                  if term.startswith('#')]
      # Count terms only (no hashtags, no mentions)
    terms_only = [term for term in preprocess(tweet['text'])
      if term not in stop and
        not term.startswith(('#', '@'))]
        # mind the ((double brackets))
        # startswith() takes a tuple (not a list) if
          # we pass a list of inputs

    terms_bigram = bigrams(terms_stop)

    # Update the counter
    # count_all.update(terms_stop)
    # count_all.update(terms_single)
    # count_all.update(terms_hash)
    count_all.update(terms_only)
    # count_all.update(terms_bigram)

  # Print the first 5 most frequent words
  # print(count_all.most_common(10))


# Term co-occurrences
# word disambiguation or semantic similarity
# Build a co-occurrence matrix com such that com[x][y] contains the number of times the term x has been seen in the same tweet as the term y:
# scipy.sparse for building a sparse matrix.

  com = defaultdict(lambda : defaultdict(int))

with open(fname, 'r') as f:
  # f is the file pointer to the JSON data set
  for line in f:
    tweet = json.loads(line)
    terms_only = [term for term in preprocess(tweet['text'])
      if term not in stop and
        not term.startswith(('#', '@'))]
    # Build co-occurrence matrix
    for i in range(len(terms_only)-1):
        for j in range(i+1, len(terms_only)):
            w1, w2 = sorted([terms_only[i], terms_only[j]])
            if w1 != w2:
              com[w1][w2] += 1

  com_max = []
  # For each term, look for the most common co-occurrent terms
  for t1 in com:
      t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
      for t2, t2_count in t1_max_terms:
          com_max.append(((t1, t2), t2_count))
  # Get the most frequent co-occurrences
  terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
  print(terms_max[:5])

  # search_word = sys.argv[1] # pass a term as a command-line argument
  # count_search = Counter()
  # for line in f:
  #    tweet = json.loads(line)
  #    terms_only = [term for term in preprocess(tweet['text'])
  #                  if term not in stop
  #                  and not term.startswith(('#', '@'))]
  #    if search_word in terms_only:
  #        count_search.update(terms_only)
  # print("Co-occurrence for %s:" % search_word)
  # print(count_search.most_common(20))

