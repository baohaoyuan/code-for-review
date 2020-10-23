#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pyLDAvis


# In[14]:


import matplotlib
import matplotlib.pyplot as plt


# In[1]:


import tweepy
import pandas as pd
import os
import csv
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

import numpy as np
import re
import warnings

#Visualisation
import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns
from IPython.display import display
#import basemap
from wordcloud import WordCloud, STOPWORDS

#nltk
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize

#matplotlib.style.use('ggplot')
pd.options.mode.chained_assignment = None
warnings.filterwarnings("ignore")

import datetime
now=datetime.datetime.utcnow().strftime('%Y_%m_%d')


# Consumer keys and access tokens, used for OAuth

consumer_key = "jCuMds8hkjry8JV8JDEuDVH9o"
consumer_secret = "psgKB7nb05kZqoD2ZFPrG78OqbObHySWUEhcLFcZ03qVMlsCwp"
access_token = "814999527451148288-PVho6BBmmcQbSVKOHBt3E5jbPJM6Krl"
access_token_secret = "a30jMaE70P2kefPFOzrfGTlA06okUcifkjJB9g2JWq4Ih"

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

#api = tweepy.API(auth)

# Sample method, used to update a status
#api.update_status('Hello Python Central!')


# In[3]:


os.chdir('/Users/vn060tw/Documents')
os.getcwd()
print(os.getcwd())


# In[20]:


#Returns the authenticated user’s information.
api.me()  


# In[4]:


api.followers()


# In[ ]:


'''public_tweets = api.home_timeline()
for tweet in public_tweets:
    print (tweet.text)
    '''


# In[3]:


user = api.get_user('asda')
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.friends_count))


# In[6]:


print(user.screen_name)
print (user.followers_count)
for friend in user.friends():
   print (friend.screen_name)


# In[ ]:


'''for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
    print(follower.screen_name)'''
    


# In[7]:


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

for follower in limit_handled(tweepy.Cursor(api.followers).items()):
    if follower.friends_count < 300:
        print(follower.screen_name)


# In[ ]:


username = ["asda", "sainsburys"]


# In[ ]:


# Create a generic dictionary for holding all tweet information
'''tweet_data = {
    "tweet_source": [],
    "tweet_text": [],
    "tweet_date": [],
    "tweet_vader_score": [],
    "tweet_neg_score": [],
    "tweet_pos_score": [],
    "tweet_neu_score": []
}
'''


# In[6]:


username='sainsburys'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
    # Access to user's access key and access secret 
auth.set_access_token(access_token, access_token_secret) 
  
    # Calling api 
api = tweepy.API(auth)
    #api = tweepy.API(auth,wait_on_rate_limit=True)
  


# In[8]:


csvFile = open(str(username)+str(now)+'.csv', 'a')

    #Use csv writer
csvWriter = csv.writer(csvFile,delimiter='|')

for tweet in tweepy.Cursor(api.search, 
                               q = username,
                               since = "2020-03-01",
                               until = now,
                               lang = "en").items():
         # Write a row to the CSV file using encode UTF-8
    csvWriter.writerow([tweet.created_at,tweet.user.screen_name,tweet.user.location, tweet.text])
    print (tweet.created_at,tweet.user.screen_name, tweet.user.location,tweet.text)
csvFile.close()
 


# In[ ]:


working code:


# In[16]:


def get_tweets(username): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_token, access_token_secret) 
  
        # Calling api 
        api = tweepy.API(auth,wait_on_rate_limit=True) 
  
        # 200 tweets to be extracted 
        # Open/create a file to append data to
        csvFile = open(str(username)+str(now)+'.csv', 'a')

        #Use csv writer
        csvWriter = csv.writer(csvFile,delimiter='|')

        for tweet in tweepy.Cursor(api.search,
                                   q = username,
                                   since = "2020-04-01",
                                   until = "2020-04-07",
                                   count=100,
                                   result_type="recent",
                                   include_entities=True,
                                   lang = "en").items():

            # Write a row to the CSV file using encode UTF-8
            csvWriter.writerow([tweet.created_at,tweet.user.screen_name,tweet.user.location, tweet.text])
            print (tweet.created_at,tweet.user.screen_name, tweet.user.location,tweet.text)
        csvFile.close()


# In[17]:


get_tweets('asda')


# In[18]:


get_tweets('sainsburys')


# In[ ]:





# In[21]:


'''import tweepy
import pandas as pd
import os
import csv

import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

now=datetime.datetime.utcnow().strftime('%Y_%m_%d')
os.chdir('/Users/vn060tw/Documents')
os.getcwd()
print(os.getcwd())
# Consumer keys and access tokens, used for OAuth

consumer_key = "jCuMds8hkjry8JV8JDEuDVH9o"
consumer_secret = "psgKB7nb05kZqoD2ZFPrG78OqbObHySWUEhcLFcZ03qVMlsCwp"
access_token = "814999527451148288-PVho6BBmmcQbSVKOHBt3E5jbPJM6Krl"
access_token_secret = "a30jMaE70P2kefPFOzrfGTlA06okUcifkjJB9g2JWq4Ih"

# set twitter data  library    

tweet_data = {"created_at": [],"screen_name": [],"location": [],"tweet_text": []} 

def get_tweets_json(username): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_token, access_token_secret) 
  
        # Calling api 
        api = tweepy.API(auth,wait_on_rate_limit=True) 
       
        for tweet in tweepy.Cursor(api.search,
                                   q = username,
                                   since = "2020-04-01",
                                   until = "2020-04-06",
                                   count=100,
                                   result_type="recent",
                                   lang = "en").items():

            tweet_data["created_at"].append(tweet.created_at)
            tweet_data["screen_name"].append(tweet.user.screen_name)
            tweet_data["location"].append(tweet.user.location)
            tweet_data["tweet_text"].append(tweet.text)
       
        with open(str(username)+str(now)+'.json', 'w') as outfile:
            json.dump(tweet_data, outfile)

'''
     


# In[ ]:


'''import json
with open('data.txt', 'w') as outfile:
  json.dump(data, outfile)'''


# In[ ]:


tweet_df = pd.DataFrame(tweet_data, columns=["created_at", 
                                             "screen_name", 
                                             "location",
                                             "tweet_text"])


# In[4]:





# In[12]:


col_names=['created_at','screen_name','location', 'text']
asda=pd.read_csv('asda2020_04_06.csv', sep='|',header=None, names=col_names)


# In[6]:


asda.head()


# In[7]:


asda.tail()


# In[8]:


#HappyEmoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])


# In[9]:


# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])


# In[10]:


#Emoji patterns
emoji_pattern = re.compile("["
         u"\U0001F600-\U0001F64F"  # emoticons
         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
         u"\U0001F680-\U0001F6FF"  # transport & map symbols
         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
         u"\U00002702-\U000027B0"
         u"\U000024C2-\U0001F251"
         "]+", flags=re.UNICODE)


# In[11]:


#combine sad and happy emoticons
emoticons = emoticons_happy.union(emoticons_sad)


# In[76]:


#Preprocessing del RT @blablabla:
asda['tweetos'] = '' 

#add tweetos first part
for i in range(len(asda['text'])):
    try:
        asda['tweetos'][i] = asda['text'].str.split(' ')[i][0]
    except AttributeError:    
        asda['tweetos'][i] = 'other'

#Preprocessing tweetos. select tweetos contains 'RT @'
for i in range(len(asda['text'])):
    if asda['tweetos'].str.contains('@')[i]  == False:
        asda['tweetos'][i] = 'other'

# remove URLs, RTs, and twitter handles
for i in range(len(asda['text'])):
    asda['text'][i] = " ".join([word for word in asda['text'][i].split()
                                if 'http' not in word and '@' not in word and '<' not in word])


asda['text'][1]


# In[ ]:


asda['text'] = asda['text'].apply(lambda x: re.sub('[!@#$:).;,?&]', '', x.lower()))
asda['text'] = asda['text'].apply(lambda x: re.sub('  ', ' ', x))
asda['text'][1]


# In[ ]:


t=asda['text']


# In[63]:


stop_words = ["https", "co", "RT","marcus","rashford","helped","raise","20m","manchester","based",
              "charity","asda","fareshare","due","today","people","citizen","still","will","larkhall",
             "tesco","nhs","hi","bbc","us","bloodcancer","told","got","ad","going","go","back","went","RT"
             ] + list(STOPWORDS)


# In[75]:


def wordcloud(tweets,col):
    stopwords = set(stop_words)
    wordcloud = WordCloud(background_color="white",stopwords=stopwords,random_state = 2020).generate(" ".join([i for i in asda[col]]))
    plt.figure( figsize=(500,250), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("Asda Sentiment Analysis")
wordcloud(asda,'text')  


# In[23]:


t.head()


# In[15]:


t.tail()


# In[19]:


t.shape


# In[62]:


t.to_csv('asda_text.csv', index=False, encoding='utf-8', header=True)


# In[9]:


t


# In[7]:


import pyLDAvis


# In[8]:


t = pyLDAvis.prepare(**t)


# In[ ]:




