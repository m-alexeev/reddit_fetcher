
import os 
import requests
import pprint
import re
from database import Database
from auth import Auth
import time
import math 
from datetime import datetime, timezone

#Token 
TOKEN = os.getenv("TOKEN")
URL = "https://oauth.reddit.com/r/"
DAY = datetime.strptime( datetime.strftime(datetime.today(), "%Y-%m-%d") , "%Y-%m-%d")


# TODO add "after" tag for pulling more data

def scrape(subreddit, limit, headers):
    url = URL + subreddit + "/hot?limit=" + str(limit) 
    # url = URL + subreddit + "/hot?after=t3_lhumfo"
    
    start = time.time()
    posts = requests.get(url, headers = headers).json()["data"]["children"]

    end = time.time()

    regex = r"\b[$]*[A-Z]{2,5}\b"
    
    mentioned_stocks = {"subreddit": subreddit, "stocks": []}
    for post in posts:
        data = post['data']
        date_posted = datetime.fromtimestamp(data['created'])
        
        if (abs((date_posted - DAY).days)) > 2:
            continue

        likes = data['ups'] 
        ratio = data['upvote_ratio']       

        stocks = re.findall(regex, data["title"])

        # Temp Filter
        if "DD" in stocks:
            stocks.remove("DD")
        if "WSB" in stocks:
            stocks.remove("WSB")

        if len(stocks) > 0:
            for stock in stocks:
                post_data = {"stock": None, "upvotes": likes, "like_ratio":ratio, "num_comments": data["num_comments"], "date_posted":date_posted}
                post_data["stock"] = stock
                post_data["upvotes"] = math.floor(likes / len(stocks))
                mentioned_stocks["stocks"].append(post_data)

    return mentioned_stocks    

def main():
    #Authentication setup
    auth = Auth()
    auth.setAccessToken(TOKEN)
    token = auth.getAccessToken()

    # init and clear db
    db = Database()
    # db.clearDB()

    subreddits = ["wallstreetbets", "pennystocks", "stocks"]
    headers = auth.getHeaders()

    for sub in subreddits:
        stock_list = scrape(sub, 100, headers)
        db.insert(stock_list)


if __name__ == "__main__":
    main()