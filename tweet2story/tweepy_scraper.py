import tweepy
import json
import os

def createApiInstance():
    customer_key = os.environ("TWITTER_CUSTOMER_KEY")
    consumer_secret = os.environ("TWITTER_CUSTOMER_KEY")    
    access_token = os.environ("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ("ACCESS_TOKEN_SECRET")

    if customer_key and consumer_secret \
        and access_token and access_token_secret:

        auth = tweepy.OAuthHandler(customer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api
    else:
        print("Twitter token is not set please export the keys as environment variable to access stream mode")

class TwitterStream(tweepy.StreamListener):
    def on_status(self, status):
        tweet = json.loads(json.dumps(status._json))
        return tweet

def sanitizeTweetText(tweet, urls):
    for url in urls:
        tweet = tweet.replace(str(url), "")
    return tweet

def santizeTweet(tweet, user):
    return {
        "handle": user.username,
        "id": tweet.id_str,
        "is_retweet": tweet.retweet,
        "urls": tweet.urls,
        "display_name": user.name,
        "avatar": user.profile_background_image_url_https,
        "tweet": sanitizeTweetText(tweet.tweet, tweet.urls),
    }

def getUser(id):
    user = api.get_user()
    return json.loads(json.dumps(user._json))

def fetch_tweet_from_url(url):
    url_args = url.split('/')
    status_id = int (url_args[len(url_args) - 1])
    tweet = api.get_status(status_id, tweet_mode="extended")
    tweet = json.loads(json.dumps(tweet._json))
    user = tweet["user"]
    return tweet