from tkinter.messagebox import NO
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlencode


class Pocket():
    def __init__(self):
        load_dotenv()
        self.CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
        self.MainEndPoint = "https://getpocket.com/v3/"

    def get_request_token(self, redirect_uri: str):
        self.endpoint = self.MainEndPoint + "oauth/request"
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "X-Accept": "application/json"}

        self.params = {"consumer_key": self.CONSUMER_KEY,
                       "redirect_uri": redirect_uri}

        self.request = requests.post(self.endpoint,
                                     self.params, headers=self.headers)
        return self.request.json()["code"]

    def generate_authorize_url(self, request_token: str, redirect_uri: str):
        return f'https://getpocket.com/auth/authorize?{urlencode({"request_token": request_token, "redirect_uri": redirect_uri})}'

    def get_access_token(self, request_token: str) -> requests.Response:
        self.endpoint = self.MainEndPoint + "oauth/authorize"
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                "X-Accept": "application/json"}

        self.params = {"consumer_key": self.CONSUMER_KEY,
                "code": request_token}

        access_resp = requests.post(
            self.endpoint, json=self.params, headers=self.headers)

        return access_resp

    def get_pocket_list(self, token: str, count: int, favorite: int, state: str):

        self.pocket_list_url = self.MainEndPoint + 'get/'

        self.headers = {"Content-Type": "application/json; charset=UTF-8"}

        self.params = {"consumer_key": self.CONSUMER_KEY,
                "access_token": token,
                "count": count,
                "detailType": "complete",
                "sort": "newest",
                "state": state,
                }
        
        if favorite is not None:
            self.params["favorite"] = str(favorite)

        response = requests.post(
            url=self.endpoint, json=self.params, headers=self.headers)
        return list(response.json()['list'].values())
