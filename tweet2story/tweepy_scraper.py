import tweepy
import json
import os
from tweet2story.image_renderer import drawStory


def createApiInstance():
    customer_key = os.environ.get("TWITTER_CUSTOMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CUSTOMER_SECRET")    
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    if customer_key and consumer_secret \
        and access_token and access_token_secret:
        auth = tweepy.OAuthHandler(customer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api
    else:
        print("Twitter token is not set please export the keys as environment variable to access stream mode")

class TwitterStream(tweepy.StreamListener):
    def __init__(self, color):
        super(TwitterStream, self).__init__()
        self.color = color
    
    def on_status(self, status):
        print("Received new tweet..")
        tweet = json.loads(json.dumps(status._json))
        tweet = santizeTweet(tweet, tweet["user"])
        print("Creating the story..")
        drawStory(tweet, self.color)
        return tweet

def sanitizeTweetText(tweet, urls):
    for url in urls:
        tweet = tweet.replace(str(url["url"]), "")
    return tweet

def santizeTweet(tweet, user):
    return {
        "handle": user["screen_name"],
        "id": tweet["id_str"],
        "display_name": user["name"],
        "avatar": user["profile_image_url_https"],
        "tweet": sanitizeTweetText(tweet['full_text'] if ("full_text" in tweet) else tweet['text'], tweet["entities"]["urls"]),
    }

def getUserByUsername(api, username):
    user = api.get_user(screen_name = username)
    return json.loads(json.dumps(user._json))

def fetchTweetFromUrl(url):
    url_args = url.split('/')
    status_id = int (url_args[len(url_args) - 1])
    tweet = api.get_status(status_id, tweet_mode="extended")
    tweet = json.loads(json.dumps(tweet._json))
    user = tweet["user"]
    return tweet