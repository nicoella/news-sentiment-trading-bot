from twikit import Client, build_query
from langdetect import detect
import configparser

# parse account data
config = configparser.ConfigParser()
config.read('twitter.cfg')

username = config['credentials']['username']
password = config['credentials']['password']

# initialize client
client = Client('en-US')

client.login(
    auth_info_1=username,
    password=password
)

# function filter out non-english tweets
def filter_english(tweets):
    english = []
    for tweet in tweets:
        try:
            if detect(tweet) == 'en':
                english.append(tweet)
        except:
            pass
    return english
    
# function search tweets 
def search_tweets(text, options):
    # build query
    query = build_query(text=text, options=options)
    
    # search tweets
    tweets = client.search_tweet(query, 'Top')
    
    results = []
    
    # print tweets
    for tweet in tweets:
        results.append(tweet.text)
        
    return filter_english(results)