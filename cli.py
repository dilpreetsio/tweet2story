import click
import os
import tweepy_scraper as tweepyScaraper
import twint_scraper as twintScraper
from image_renderer import draw_story, save_story
@click.command()
@click.option('-u', default ="", help="Paste url of the tweet")
# @click.option('-s', default=False, help="flag for stream mode")
# @click.option('-pro', default=False, help="flag for pro mode using tweepy")
def url_2_story(u):
    """Create beautiful stories from tweets"""
    # if(s) :
        # user = api.lookup_users(screen_names=[s])[0]
        # user = json.loads(json.dumps(user._json))
        # print("streaming tweets for " + user['name'])
        # stream_listener = TwitterStream()
        # stream = tweepy.Stream(auth = api.auth, listener=stream_listener, tweet_mode="extended")
        # stream.filter(follow=[user['id_str']])
    # if pro:
    #     print("user tweepy here")
    if u!="":
        # print(u)
        tweet = twintScraper.getTweetFromUrl(u)
        # tweet = fetch_tweet_from_url(u)
        image = draw_story(tweet)
        save_story(image, name = tweet["user"]["screen_name"] + "_" + str(tweet["id"]))
        #tweepy mode
    else:
        print("missing args")

if __name__ == '__main__':
    url_2_story()
