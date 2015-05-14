#!/usr/bin/env python
__author__ = 'William'

from tweepy.streaming import StreamListener
import json


class StreamHandler(StreamListener):

    def on_data(self, data):
        self.print_data(data)
        return True

    def on_error(self, status):
        print "ERROR", status

    def print_data(self, data):
        print data.strip('\n')
