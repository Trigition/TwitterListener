#!/usr/bin/env python

import pandas as pd
import json

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 500)

filename = "tweets.out"
tweet_file = open(filename, "r");
tweet_data = []
for line in tweet_file:
    try:
        tweet_raw = json.loads(line.strip('\n'))
        tweet_data.append(tweet_raw)
    except ValueError:
        continue
print len(tweet_data)
tweets = pd.DataFrame()
tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], tweet_data)
tweets['text'] = map(lambda tweet: tweet['text'], tweet_data)
tweets['location'] = map(lambda tweet: tweet['user']['location'], tweet_data)
# tweets['entities'] = map(lambda tweet: tweet['entities']['hashtags']['text'], tweet_data)
print tweets
