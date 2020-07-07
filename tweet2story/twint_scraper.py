import twint

def createConfig(username, last_tweet_time):
    twint_config = twint.Config()
    twint_config.Username = username
    twint_config.Store_object = True
    twint_config.Limit = 250
    twint_config.Hide_output = True
    twint_config.User_full = True
    if last_tweet_time != None:
        twint_config.Until = "" + last_tweet_time
    return twint_config

def getUserByUsername(username):
    user_config = twint.Config()
    user_config.Username = username
    user_config.Store_object = True
    user_config.Hide_output = True
    twint.run.Lookup(user_config)
    user = twint.output.users_list
    return user[0]

def sanitizeTweetText(tweet, urls):
    for url in urls:
        tweet = tweet.replace(str(url), "")
    return tweet

def sanitizeTweet(tweet, user):
    return {
        "handle": tweet.username,
        "id": tweet.id_str,
        "is_retweet": tweet.retweet,
        "urls": tweet.urls,
        "display_name": user.name,
        "avatar": user.avatar,
        "tweet": sanitizeTweetText(tweet.tweet, tweet.urls),
    }

def getTweetFromUrl(url):
    url_array = url.split("/")
    tweet_id = url_array[5]
    username = url_array[3]
    if "?" in tweet_id:
        tweet_id = tweet_id.split("?")[0]
    last_tweet_time = None
    tweet_found = False
    user = getUserByUsername(username)

    while not tweet_found:
        twint.run.Search(createConfig(username, last_tweet_time))
        tweets = twint.output.tweets_list

        for tweet in tweets:
            if tweet.id_str == tweet_id:
                return sanitizeTweet(tweet, user)
                tweet_found = True

        last_tweet_time = tweets[len(tweets)-1].datestamp