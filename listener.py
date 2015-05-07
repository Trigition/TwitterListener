#!/usr/bin/env python
__author__ = 'William'

import argparse
from tweepy import OAuthHandler
from tweepy import Stream
from stream_handler import StreamHandler

# Format for 'secret' file:
# Consumer Key
# Consumer Secret
# Access Token
# Access Token Secret

parser = argparse.ArgumentParser(description='This script listens to the Public Streams from Twitter')
parser.add_argument('--secret', '-s', help='Secrets File for Twitter API', required=True)

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

print "Creating Listener"
listener = StreamHandler()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
twitter_stream = Stream(auth, listener)

twitter_stream.filter(track=['python', 'javascript', 'ruby'])