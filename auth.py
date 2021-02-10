import requests, requests.auth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT = os.getenv("CLIENT")
SECRET = os.getenv("SECRET")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


class Auth: 
    username = CLIENT
    password = PASSWORD
    client = CLIENT
    secret = SECRET
    token = None

    headers = {"User-Agent": "fetcher/0.0.1"}

    def generateAccessToken(self):
        auth = requests.auth.HTTPBasicAuth(CLIENT, SECRET)
        data = {'grant_type': 'password',
            'username': self.username,
            'password': self.password }

        headers = {"User-Agent": "fetcher/0.0.1", "Content-type": "application/x-www-form-urlencoded"}
        token_url = 'https://www.reddit.com/api/v1/access_token'

        res = requests.post(token_url, auth = auth, data=data, headers=headers)
        if ("error" not in res.json()):
            self.token = res.json()["access_token"]
            self.headers = {**headers, **{'Authorization': f"bearer {self.token}"}}
            return self.token


    def setAccessToken(self, token):
        os.environ["TOKEN"] = token
        self.token = token
        self.headers["Authorization"] = f"bearer {self.token}"

    def getAccessToken(self):
        return self.token

    def getHeaders(self):
        return self.headers
    