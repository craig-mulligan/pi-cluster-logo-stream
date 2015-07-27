import os
import urllib
import subprocess
import tweepy
from tweepy import StreamListener
from tweepy import Stream

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
key_word = os.getenv('HASHTAG', 'testpicluster')

def get_image():
	search_text = "#" + key_word
	search_number = os.getenv('TOTAL', 24)
	search_result = api.search(search_text, count=search_number)

	index = int(os.getenv('INDEX', 0))
	total = len(search_result)

	print "total return " + str(total)
	print "index " + str(index)
	if index < total:
		domain = search_result[index].entities['urls'][0]['display_url']
		if domain == None:
			print "no url provided"
		else: 
			print domain
			url = 'https://logo.clearbit.com/' + domain
			urllib.urlretrieve(url, "../data/logo.png")
			subprocess.Popen(['sh','/app/image.sh'], stdout=subprocess.PIPE)
	else:
		print "Not enough tweets :("

class StdOutListener(StreamListener):
	
    def on_data(self, data):
        # process stream data here
        print ("New tweet!")
        get_image()

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    print "Listening for free ads"

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth, l)
    stream.filter(track=[key_word])