#!/usr/bin/env python

import pandas as pd
import json
import glob
import os
import argparse
import GlamourPrint
import json
from nltk.corpus import treebank

parser = argparse.ArgumentParser(description="This script performs data analysis on archived tweets.")
parser.add_argument("--tweet", "-t", help="Twitter filepath", default="all_tweets.tweet")
parser.add_argument("--consolidate", "-c", help="Consolidate tweet filename", default=None)
parser.add_argument("--search", "-s", help="Filters for consolidating files", default=None, nargs="*")
args = parser.parse_args()

def consolidate_tweet_files(path, fileout_name, search):
    # Open consolidate file
    file_out = open(fileout_name, "w")

    # Save current directory
    prev_dir = os.getcwd()
    os.chdir(path)
    tweet_files = glob.glob('*.tweet')
    for tweet in tweet_files:
        tweet_file = open(tweet)
        for tweet_str in tweet_file:
            if check_tweet(tweet_str, search):
                file_out.write(tweet_file.read().strip('\n'))
                file_out.write('\n')
        tweet_file.close()
    os.chdir(prev_dir)
    file_out.close()

def check_tweet(tweet_str, search):
    tweet_json = json.loads(tweet_str)
    for rule in search:
        try:
            tweet_json[rule]
        except KeyError:
            return False
    return True

def load_tweets(filename):
    file_in = open(filename, "r")
    tweet_json = []
    for line in file_in:
        tmp_json = json.loads(line)
        GlamourPrint.reprint("Loading: " + tmp_json['id_str'])
        tweet_json.append(tmp_json)
    return tweet_json

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 100)

if args.consolidate is not None:
    consolidate_tweet_files("./tweets/", args.consolidate, args.search)

tweet_data = load_tweets(args.tweet)

tweets = pd.DataFrame()
tweets['user'] = map(lambda tweet: tweet['user']['name'], tweet_data)
tweets['username'] = map(lambda tweet: tweet['user']['screen_name'], tweet_data)
tweets['text'] = map(lambda tweet: tweet['text'], tweet_data)
tweets['location'] = map(lambda tweet: tweet['user']['location'], tweet_data)
tweets['place'] = map(lambda tweet: tweet['place'], tweet_data)
# tweets['friends_count'] = map(lambda tweet: tweet['user']['friends_count'], tweet_data)
# tweets['decription'] = map(lambda tweet: tweet['user']['description'], tweet_data)
# tweets['retweets'] = map(lambda tweet: tweet['retweet_count'], tweet_data)
# tweets['entities'] = map(lambda tweet: tweet['entities']['hashtags']['text'], tweet_data)
# tweets['filter'] = map(lambda tweet: tweet['filter_level'], tweet_data)
print tweets
print "Number of Tweets:", len(tweet_data)
