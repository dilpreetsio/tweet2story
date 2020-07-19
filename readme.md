# Tweet2Story
![Intro Gif](https://github.com/dilpreetsio/tweet2story/blob/master/tweet2story.gif) <br/>
Create instagram stories from tweets using cli.<br/>
![Elon Sample](https://github.com/dilpreetsio/tweet2story/blob/master/elonmusk_sample.png)
![Naval Sample](https://github.com/dilpreetsio/tweet2story/blob/master/naval_sample.png)
![Mr beast Sample](https://github.com/dilpreetsio/tweet2story/blob/master/mrbeastyt_sample.png)
![Orange Sample](https://github.com/dilpreetsio/tweet2story/blob/master/orangebook_sample.png)
![Stoic Sample](https://github.com/dilpreetsio/tweet2story/blob/master/stoic_sample.png)

## Requirements 
* [Pillow](https://pillow.readthedocs.io/en/stable/) 
* [Tweepy](https://www.tweepy.org/) 
* [Click](https://click.palletsprojects.com/en/7.x/) 
* [Twint](https://github.com/twintproject/twint)

## Commands

### Create a story using a url 
```
tweet2story -u <URL OF THE TWEET>
```

### Start a streamer (requires API keys to be exported)
```
tweet2story -s <USERNAME>
```
#### This requires creating a twitter app from developer console & exporting credentials.

Set environment variables 
```
TWITTER_CUSTOMER_KEY = Customer key of the created app
TWITTER_CUSTOMER_SECRET = Customer secret of the created app
TWITTER_ACCESS_TOKEN = Access token of the created app
TWITTER_ACCESS_TOKEN_SECRET = Access secret of the created app
```

## Options 

Flag | Description
------------ | -------------
-u | Flag for url mode uses TWINT to generate the tweet no API integration required
-s | Flag for streamer mode REQUIRES API KEYS
-c | Set background color of the tweet from these colors orange, red, green, yellow, violet, blue, pink

## Roadmap
- [ ] Add media support in tweets
- [ ] Add thread support


## License 
MIT