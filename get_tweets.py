# get_tweets.py
# This script pulls tweets from an inputed twitter user and saves them to a file in ./src
#
# Usage: get_tweets.py [Twitter handle]

import markovify
import requests
import sys
import os, json
from config import settings    #import authorization settings
from requests_oauthlib import OAuth1

# Sets API parameters from OAuthSettings (private)

CONSUMER_KEY = settings['consumer_key']
CONSUMER_SECRET = settings['consumer_secret']
ACCESS_TOKEN = settings['access_token_key']
ACCESS_SECRET = settings['access_token_secret']

if (len(sys.argv) != 2):
	print "Usage: get_tweets.py [Twitter handle]"
	sys.exit()

screen_name = sys.argv[1]
if requests.get('https://twitter.com/' + screen_name).status_code == 404:
	print "Looks like that username doesn't exist. Make sure the inputed username is valid"
	sys.exit()

oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# Get first 200 (minus # of RTs) tweets
payload = {'screen_name':screen_name,'include_rts':False,'count':200}
timeline = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', auth=oauth, params=payload).json()
full_timeline = []

# Max_id paginate through rest of tweets, up to theoretical limit of 3200
for i in xrange(16):
	max_id = timeline[-1]['id'] - 1
	payload = {'screen_name':screen_name,'include_rts':False,'count':200,'max_id':max_id}
	timeline = requests.get('https://api.twitter.com/1.1/statuses/user_timeline.json', auth=oauth, params=payload).json()
	full_timeline += timeline

# Write tweets to src file
tweetfile = open('src/'+screen_name+'.txt', 'w')
for tweet in full_timeline:
	tweetfile.write(tweet['text'].encode('utf-8') + '\n')
