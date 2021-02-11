
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




def scrape(subreddit, limit, headers):
    url = URL + subreddit + "/hot?limit=" + str(limit)
    start = time.time()
    posts = requests.get(url, headers = headers).json()["data"]["children"]
    end = time.time()

    regex = "\$*[A-Z][A-Z]+"
    
    mentioned_stocks = {"subreddit": subreddit, "stocks": []}
        
    for post in posts:

        data = post['data']
        date_posted = datetime.fromtimestamp(data['created'])
        
        if (abs((date_posted - DAY).days)) > 2:
            continue

        likes = data['ups'] * data['upvote_ratio']       

        stocks = re.findall(regex, data["title"])
        if "DD" in stocks:
            stocks.remove("DD")
        if len(stocks) > 0:
            for stock in stocks:
                post_data = {"stock": None, "upvotes": likes, "num_comments": data["num_comments"]}
                post_data["stock"] = stock
                post_data["upvotes"] = math.floor(likes / len(stocks))
                mentioned_stocks["stocks"].append(post_data)

    print(mentioned_stocks)


def main():
    #Authentication setup
    auth = Auth()
    auth.setAccessToken(TOKEN)
    token = auth.getAccessToken()


    subreddits = ["wallstreetbets", "pennystocks", "stocks"]
    headers = auth.getHeaders()

    for sub in subreddits:
        scrape(sub, 1, headers)


    db = Database()


if __name__ == "__main__":
    main()