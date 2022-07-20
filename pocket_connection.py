import pocket
import db_connection
import requests
import json
import os

consumer_key = os.getenv('CONSUMER_KEY')
redirect_uri = os.getenv('REDIRECT_URI')


def get_client(discord_user_id):
    client = pocket.Pocket(
        consumer_key=consumer_key,
        access_token=str(db_connection.get_user('725329093889097811')[1]),
    )
    return client


def generate_request_token():
    pocket_get_request_token_url = "https://getpocket.com/v3/oauth/request"
    headers = {"Content-Type": "application/json; charset=UTF-8",
               "X-Accept": "application/json"}

    params = {"consumer_key": consumer_key,
              "redirect_uri": "https://example.com"}

    pocket_oauth = requests.post(pocket_get_request_token_url,
                                 json=params, headers=headers)

    request_token = json.loads(pocket_oauth.text)["code"]
    return request_token


def generate_authorize_url(request_token):
    request_url = f'https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=https://seyedmm.github.io/authorized.html'
    return request_url


def generate_access_token(request_token):
    pocket_get_access_token_url = "https://getpocket.com/v3/oauth/authorize"
    headers = {"Content-Type": "application/json; charset=UTF-8",
               "X-Accept": "application/json"}

    params = {"consumer_key": consumer_key,
              "code": request_token}

    access_resp = requests.post(pocket_get_access_token_url,
                                json=params, headers=headers)

    access_token = access_resp.text
    return access_token
