import tweepy
import json



def createApiInstance():
    auth = tweepy.OAuthHandler('', '')
    auth.set_access_token('', '')
    api = tweepy.API(auth)
    return api

class TwitterStream(tweepy.StreamListener):
    def on_status(self, status):
        tweet = json.loads(json.dumps(status._json))
        return tweet
        # image = draw_story(tweet)
        # save_story(image, name = tweet["user"]["screen_name"] + "_" +str(tweet["id"]))

def getUser():
    print("get user")

def fetch_tweet_from_url(url):
    url_args = url.split('/')
    status_id = int (url_args[len(url_args) - 1])
    tweet = api.get_status(status_id, tweet_mode="extended")
    tweet = json.loads(json.dumps(tweet._json))
    return tweet