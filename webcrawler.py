from datetime import datetime
from bs4 import BeautifulSoup
import requests
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

# constants
DEFAULT_QUERY = "US+SPX+500"

# webcrawler to crawl google news
def crawl_news(date=None, query=DEFAULT_QUERY):
    # check if the result is already memoized
    cache_key = (query, date)  
    if cache_key in memoized_searches:
        print("memoized")
        return memoized_searches[cache_key]
    
    # set date to today if not specified
    if (date == None):
        date = datetime.now().strftime("%m/%d/%Y")
    
    # loop through pages until date reached
    page = 0
    news = []
    
    while True:
        # create base URL for current page
        base_url = "https://www.google.com/search?q="+query+"&tbs=cdr:1,cd_max:"+date+",sbd:1&tbm=nws&start="+str(page)
        page += 10
        
        # HTTP GET request
        response = requests.get(base_url)
        
        # exit if a date is reached
        exit = False
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # find all articles on the current page
            articles = soup.find_all("div", class_="Gx5Zad fP1Qef xpd EtOod pkphOe")
                
            # iterate through each article    
            for article in articles:
                title = article.find("div", class_="BNeawe vvjwJb AP7Wnd").text.strip()
                date = article.find("span", class_="r0bn4c rQMQod").text.strip()
                
                # exit once 2 months or more reached
                split = date.split(' ')
                if (split[1] == "months" or split[1] == "year" or split[1] == "years"):
                    exit = True
                    break
                news.append(title)
        else:
            print("error fetching news articles. status code:", response.status_code)
            break
        
        if exit:
            break
        
    # memoize results
    memoized_searches[cache_key] = news
    save_memoized_searches()
    
    # return results
    return news
    
print(crawl_news())