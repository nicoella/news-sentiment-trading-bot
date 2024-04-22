from twikit import Client, build_query
from langdetect import detect
import configparser
import pickle

# save memoized data
memoized_searches = {}

# retrieve memoized searches
def load_memoized_searches():
    try:
        with open("memoized_searches.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}
    
# save memoized searches
def save_memoized_searches():
    with open("memoized_searches.pkl", "wb") as file:
        pickle.dump(memoized_searches, file)
        
# load initially saved data
memoized_searches = load_memoized_searches()

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
    # check if the result is already memoized
    cache_key = (text, options.get('date'))  
    if cache_key in memoized_searches:
        print("memoized")
        return memoized_searches[cache_key]
    
    # build query
    query = build_query(text=text, options=options)
    
    # search tweets
    tweets = client.search_tweet(query, 'Top')
    
    results = []
    
    # print tweets
    for tweet in tweets:
        results.append(tweet.text)
        
    filtered_results = filter_english(results)
    
    # memoize results
    memoized_searches[cache_key] = filtered_results
    
    # save memoized results to file
    save_memoized_searches()
    
    # return results
    return filtered_results