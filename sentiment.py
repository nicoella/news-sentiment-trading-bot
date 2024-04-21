from textblob import TextBlob
from webcrawler import search_tweets

# constants
QUERY = "#SPX500"

# function to calculate the sentiment of a tweet
def sentiment(text):
    analysis = TextBlob(text)
    
    polarity = analysis.sentiment.polarity
    
    return polarity
    
# function to calculate buy, sell, or neutral
def total_sentiment(date):
    tweets = search_tweets(QUERY, { date: date })
    
    sum = 0
    for tweet in tweets:
        sum += sentiment(tweet)
        
    sum /= len(tweets)

    if sum > 0.1: # stock is rising
        return 1
    elif sum < -0.1: # stock is dropping
        return -1
    else: # neutral
        return 0
