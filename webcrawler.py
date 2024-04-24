from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# constants
DEFAULT_QUERY = "US+SPX+500"

# set up driver
chrome_options = Options()
chrome_options.add_argument("--headless")  
service = Service('./chromedriver')  # update path to chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

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

# generate start date as range days before date_str separated by separator
def generate_start_date(date_str, range, separator):
    # convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%m"+separator+"%d"+separator+"%Y")
    
    # subtract range # of days from the date
    one_month_ago = date_obj - timedelta(days=range)
    
    # return the result as a string in the same format
    return one_month_ago.strftime("%m"+separator+"%d"+separator+"%Y")

# generate param str from param object
def generate_param_str(params):
    param_str = ''
    for param in params:
        param_str += param + "=" + params[param] + "&"
    return param_str

# crawl google news
def crawl_google(date):
    if (date == None):
        date = datetime.now().strftime("%m/%d/%Y")
    start_date = generate_start_date(date, 7, '/')
    link = "https://www.google.com/search"
    params = {
        'q':DEFAULT_QUERY, 'tbs':'cdr:1,cd_min:'+start_date+',cd_max:'+date+',sbd:1', 'tbm':'nws', 
    }
    return crawl(link, 'start', 10, params, "div", "SoaBEf", '.n0jPhd.ynAwRc.MBeuO.nDgy9d')

# general webcrawler function
def crawl(link, page_param, page_iterator, params, container_type, container_class = None, title_class = None):
    # check if query is memoized
    cache_key = f"{link}?{generate_param_str(params)}"
    if cache_key in memoized_searches:
        return memoized_searches[cache_key]  
    
    news = []
    page = 0
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    service = Service('./chromedriver')  # update path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # loop all pages
    while True:
        # generate url
        params[page_param] = str(page)
        url = f"{link}?{generate_param_str(params)}"
        page += page_iterator
        
        # query url
        driver.get(url)
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, container_type)))

        # parse html
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all(container_type, class_=container_class) if container_class is not None else soup.find_all(container_type)
           
        # exit when no more articles 
        if (len(articles) == 0):
            break
            
        # iterate over each article and extract titles
        for article in articles:
            article_title = article.select_one(title_class).text.strip() 
            news.append(article_title)
    
    # quit driver
    driver.quit()
    
    # memoize results
    memoized_searches[cache_key] = news
    save_memoized_searches()
    
    # return results
    return news
