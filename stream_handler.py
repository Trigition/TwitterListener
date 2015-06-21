#!/usr/bin/env python
__author__ = 'William'

from tweepy.streaming import StreamListener
import json
import sys
from time import gmtime, strftime


class StreamHandler(StreamListener):

    def __init__(self):
        super(StreamHandler, self).__init__()
        self.prev_time = strftime("%H", gmtime())

    def on_connect(self):

        pass

    def on_data(self, data):
        self.print_data(data)
        return True

    def on_error(self, status):
        print "ERROR", status

    def print_data(self, data):
        #Todo spawn process to write tweet
        current_hour = strftime("%H", gmtime())
        if current_hour != self.prev_time:
            print current_hour, self.prev_time
            self.prev_time = current_hour
            raise RefreshWarning("Refreshed")
        try:
            file_out = None
            date_hour = str(strftime("%d_%b_%Y_%H", gmtime()))
            filename = "./tweets/" + date_hour + ".tweet"
            try:
                file_out = open(filename, "a")
            except IOError:
                file_out = open(filename, "w")
            tweet = json.loads(data)
            try:
                if tweet['coordinates'] is not None:
                    str_out = "\rTweet received on: %s from %s\n" % (tweet['created_at'], tweet['coordinates'])
                    sys.stdout.write(str_out)
                    sys.stdout.flush()
                else:
                    reprint_string = "\rTweet #%s on %s" % (tweet['id_str'], tweet['created_at'])
                    sys.stdout.write(reprint_string)
                    sys.stdout.flush()
            except KeyError:
                reprint_string = "\rTweet received on: %s" % tweet['created_at']
                sys.stdout.write(reprint_string)
                sys.stdout.flush()
            file_out.write(data.strip('\n'))
            file_out.write("\n")
            file_out.close()
        except KeyError:
            # print "Tweet error! Ignoring"
            return

class RefreshWarning(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
