import click
import os
import tweepy
import tweet2story.tweepy_scraper as tweepyScaraper
from tweet2story.tweepy_scraper import TwitterStream, fetchTweetFromUrl
import tweet2story.twint_scraper as twintScraper
from tweet2story.image_renderer import drawStory, saveStory

colors = {
    "twitter": (29, 161, 242),
    "orange": (255, 163, 0),
    "red": (218, 75, 92),
    "green": (180,238,180),
    "yellow":(255, 223, 124),
    "violet":(134, 0, 125),
    "blue": (149, 201, 225),
    "pink": (246, 169, 189)
}

@click.command()
@click.option('-u', default ="", help="Use -u flag to create a new story from a url")
@click.option('-s', default=False, help="Use -s flag for stream mode followed by the user name of the twitter user. Required twitter api access")
@click.option('-c', default=False, help="Background color of the tweet, you can choose from blue, red, orange, green, yellow & violet")
def main(u, s, c):
    """Create beautiful stories from tweets"""
    if u!="":
        print("Fetching tweet..")
        tweet = twintScraper.getTweetFromUrl(u)
        print("Creating story..")
        drawStory(tweet, colors[c] if c in colors else colors["twitter"])
    elif(s) :
        if os.environ.get("TWITTER_CUSTOMER_KEY") and os.environ.get("TWITTER_CUSTOMER_SECRET") and\
           os.environ.get("TWITTER_ACCESS_TOKEN") and os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"):
            stream_listener = TwitterStream(colors[c] if c in colors else colors["twitter"])
            api = tweepyScaraper.createApiInstance()
            user = tweepyScaraper.getUserByUsername(api, s)
            print("Streaming tweets by " + s)
            stream = tweepy.Stream(auth = api.auth, listener=stream_listener, tweet_mode="extended")
            stream.filter(follow=[user['id_str']])
        else:
            click.echo(click.style("Error", fg="red") +''': You are trying to use stream mode which requires adding twitter api keys as environment variables.
             Please set up a new twitter app & add the credentials here. set up app here ''' + click.style("https://developer.twitter.com/apps", fg ="blue"))
    
    else:
        click.echo(click.style("Missing arguments", fg="red") +''': please do tweet2story --help, to learn more about tweet2story''')

if __name__ == '__main__':
    main()
