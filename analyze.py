#!/usr/bin/env python
__author__= "William"

import pandas as pd
import time
import json
from bokeh.charts import TimeSeries, output_file, show

def extract_hashtags(entities):
    tmp_str = entities
    if entities is None:
        return None
    try:
        # print tmp_str
        entity = json.loads(tmp_str)
        # print entity['hashtags'][0]['text']
        hashtags = []
        for hashtag in entity['hashtags']:
            #print "Hashtag:", hashtag['text']
            hashtags.append(hashtag['text'])
        return hashtags
    except TypeError:
        # print "Returning none..."
        return None
    except IndexError:
        return None
    except ValueError:
        print "Improper JSON string:", tmp_str
        return None

def extract_trends(entities):
    tmp_str = entities
    if entities is None:
        return None
    try:
        entity = json.loads(tmp_str)
        trends = []
        for trend in entity['trends']:
            trends.append(trend['text'])
        return trends
    except TypeError:
        return None

tweet_df = pd.DataFrame.from_csv("filtered.csv")

# Perform extraction and formatting of data
tweet_df['hashtags'] = tweet_df['entities'].apply(extract_hashtags)
tweet_df.index = pd.to_datetime(tweet_df.pop("date"))
