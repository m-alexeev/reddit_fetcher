import auth
import os 
import requests
import pprint


auth = auth.Auth()

TOKEN = os.getenv("TOKEN")

auth.setAccessToken(TOKEN)
token = auth.getAccessToken()


pp = pprint.PrettyPrinter(indent=1)

url = "https://oauth.reddit.com/r/stocks/hot?limit=10"

subreddits = ["wallstreetbets", "pennystocks", "stocks"]

posts = requests.get(url, headers = auth.getHeaders()).json()["data"]["children"]

for post in posts:
    print(post['data']['title'])
