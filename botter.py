import markovify
import requests
import sys, errno
import os, json
from config import settings    #import authorization settings
from requests_oauthlib import OAuth1


def get_tweets(screen_name):

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
		if timeline == []:
			break
		full_timeline += timeline

	# Write tweets to src file
	tweetfile = open('src/'+screen_name+'.txt', 'w')
	for tweet in full_timeline:
		tweetfile.write(tweet['text'].encode('utf-8') + '\n')



# Sets API parameters from OAuthSettings (private)

CONSUMER_KEY = settings['consumer_key']
CONSUMER_SECRET = settings['consumer_secret']
ACCESS_TOKEN = settings['access_token_key']
ACCESS_SECRET = settings['access_token_secret']

if (len(sys.argv) != 2):
	print "Usage: botter.py [Twitter handle]"
	sys.exit()

screen_name = sys.argv[1]

if not os.path.exists(os.path.dirname('src/'+screen_name)):
    try:
        os.makedirs(os.path.dirname('src/'+screen_name))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise
# thanks https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output

# If source doesn't exist for user, make one
if not os.path.isfile('src/'+screen_name+'.txt'):
	get_tweets(screen_name)

tweetfile = open('src/'+screen_name+'.txt','r')
model = markovify.NewlineText(tweetfile.read())
tweet = model.make_short_sentence(140)

print tweet