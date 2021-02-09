import requests
import os

CLIENT = os.getenv("CLIENT")
SECRET = os.getenv("SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


auth = requests.auth.HTTPBasicAuth(CLIENT, SECRET)


data = {'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD,}

headers = {"User-Agent": "fetcher/0.1"}
token_url = 'https://www.reddit.com/api/v1/access_token'

res = requests.post(token_url, auth = auth, data=data, headers=headers)

print(res.json())