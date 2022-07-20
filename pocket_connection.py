import pocket
import db_connection
import requests
import json
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
redirect_uri = os.getenv('REDIRECT_URI')


def get_client(discord_user_id):
    client = pocket.Pocket(
        consumer_key=CONSUMER_KEY,
        access_token=str(db_connection.get_user('725329093889097811')[1]),
    )
    return client


def generate_request_token():
    pocket_get_request_token_url = "https://getpocket.com/v3/oauth/request"
    headers = {"Content-Type": "application/json; charset=UTF-8",
               "X-Accept": "application/json"}

    params = {"consumer_key": CONSUMER_KEY,
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

    params = {"consumer_key": CONSUMER_KEY,
              "code": request_token}

    access_resp = requests.post(pocket_get_access_token_url,
                                json=params, headers=headers)

    access_token = access_resp.text
    return access_token


def get_pocket_list(discord_id, count, favorite, state):
    pocket_user = db_connection.get_user(str(discord_id))

    pocket_list_url = 'https://getpocket.com/v3/get'

    headers = {"Content-Type": "application/json; charset=UTF-8"}

    params = {"consumer_key": CONSUMER_KEY,
              "access_token": pocket_user[1],
              "count": count,
              "detailType": "complete",
              "sort": "newest",
              "state": state,
              }
    if favorite == True:
        params.update({"favorite": 1})
    elif favorite == False:
        params.update({"favorite": 0})

    response = requests.post(url=pocket_list_url, json=params, headers=headers)
    raw_response_json = json.loads(response.text)
    raw_pocket_list = raw_response_json['list']
    pocket_list = list(raw_pocket_list.values())
    return pocket_list
