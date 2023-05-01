import sys
sys.path.insert(0, 'vendor')

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

PREFIX = '&'

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

def receive(event, context):
    message = json.loads(event['body'])

    bot_id = message['bot_id']
    response = process(message)
    if response:
        send(response, bot_id)

    return {
        'statusCode': 200,
        'body': 'ok'
    }

def process(message):
    # Prevent self-reply
    if message['sender_type'] == 'bot':
        return None

    if message['text'].startswith(PREFIX):
        response = sp.search(q = message['text'], type = 'track')
        reply = response['tracks']['items'][0]['external_urls']['spotify']
        return reply


def send(text, bot_id):
    url = 'https://api.groupme.com/v3/bots/post'

    message = {
        'bot_id': bot_id,
        'text': text,
    }
    r = requests.post(url, json=message)