#!/usr/bin/env python
__author__ = 'William'

import argparse
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from stream_handler import StreamHandler
from stream_handler import RefreshWarning
from urllib3.exceptions import ProtocolError
import json
import time

United_States_ID = 23424977
World_ID = 1

# Format for 'secret' file:
# Consumer Key
# Consumer Secret
# Access Token
# Access Token Secret

parser = argparse.ArgumentParser(description="This script listens to the Public Streams from Twitter")
parser.add_argument("--secret", "-s", help="Secrets File for Twitter API", required=True)
parser.add_argument("--action", "-a", help="Action to be taken", default=["stream"], nargs="*")

args = parser.parse_args()

# Open file and read in Keys and Credentials
secrets_file = open(args.secret)
CONSUMER_KEY = secrets_file.readline().strip()
CONSUMER_SECRET = secrets_file.readline().strip()
ACCESS_TOKEN = secrets_file.readline().strip()
ACCESS_SECRET = secrets_file.readline().strip()
"""
print "Consumer Key:", CONSUMER_KEY
print "Consumer Secret:", CONSUMER_SECRET
print "Access Token:", ACCESS_TOKEN
print "Access Secret:", ACCESS_SECRET"""

listener = StreamHandler()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter_stream = Stream(auth, listener)

twitter = API(auth)
world_trends = twitter.trends_place(World_ID)
US_trends = twitter.trends_place(United_States_ID)

world_trends = world_trends[0]
US_trends = US_trends[0]

search = []

if "trends" or "trend" in args.action:
    for trend in world_trends['trends']:
        print "World Trend:", trend['name']
    for trend in US_trends['trends']:
        print "US Trend:", trend['name']

for trend in world_trends['trends']:
    search.append(trend['name'])
for trend in US_trends['trends']:
    search.append(trend['name'])

backoff = 2

if "stream" in args.action:
    while(True):
        try:
            time.sleep(backoff)
            print "Creating stream..."
            twitter_stream.filter(track=search, languages=["en"])
        except RefreshWarning:
            print "New trends are required"
            search = []
            world_trends = twitter.trends_place(World_ID)
            US_trends = twitter.trends_place(United_States_ID)
            world_trends = world_trends[0]
            US_trends = US_trends[0]
            for trend in world_trends['trends']:
                search.append(trend['name'])
            for trend in US_trends['trends']:
                search.append(trend['name'])
            backoff = backoff ** 2
            continue
