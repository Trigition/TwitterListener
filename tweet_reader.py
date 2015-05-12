#!/usr/bin/env python

import pandas as pd
import json

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
tweets['text'] = map(lambda tweet: tweet['text'], tweet_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweet_data)
print tweets
