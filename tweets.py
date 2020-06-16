import tweepy
import json
import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import click
import os
import GetOldTweets3 as got

width = 1080
height = 1920
avatar_size = 300
avatar_boundry_width = 30
rectangle_padding = 40
tweet_text_height = 4
name_font_size = 60
handle_font_size = 36
tweet_text_font_size = 48
user_font_size = 10
tweet_line_height = 4

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)

class TwitterStream(tweepy.StreamListener):
    def on_status(self, status):
        tweet = json.loads(json.dumps(status._json))
        print(tweet)
        image = draw_story(tweet)
        save_story(image, name = tweet["user"]["screen_name"] + "_" +str(tweet["id"]))

def fetch_tweet_from_url(url):
    url_args = url.split('/')
    status_id = int (url_args[len(url_args) - 1])
    tweet = api.get_status(status_id, tweet_mode="extended")
    tweet = json.loads(json.dumps(tweet._json))
    return tweet

def save_story(image, name):
    image.save("./" + name + ".png")

def draw_story(tweet):
    user = tweet["user"]
    tweet_text = tweet['full_text'] if ("full_text" in tweet) else tweet['text']
    display_name = user["name"]
    handle = "@" + user["screen_name"]
    avatar_url = user["profile_image_url"]
    avatar_url = avatar_url[:avatar_url.rindex('_')] + avatar_url[avatar_url.rindex('.') :]
    print(avatar_url)
    response = requests.get(avatar_url)

    image = Image.new('RGBA', (1080, 1920), (29, 161, 242)) #bg with twitter color
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(image)

    # Calculate the dimensions
    font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", tweet_text_font_size)
    lines = textwrap.wrap(tweet_text, width=38)
    line_widths = []
    for line in lines:
        line_widths.append(font.getsize(line)[0])
    tweet_text_height = len(lines) * (font.getsize(lines[0])[1] + 5)
    tweet_text_width = max(line_widths)

    avatar_boundry = avatar_size + avatar_boundry_width

    rect_width_half = (rectangle_padding + tweet_text_width/2)
    rect_height_half = (rectangle_padding + tweet_text_height/2) + name_font_size + handle_font_size + (avatar_size /4)
    rectangle_top = (height / 2) - rect_height_half

    #Draw the tweet image
    draw.rectangle([ width /2 - rect_width_half,
                    height / 2 - rect_height_half, 
                    width /2 + rect_width_half, 
                    height/2 + rect_height_half], 
                    width=0, fill=(256,256,256))

    #create a circular avatar image
    mask = Image.new("L", avatar.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, avatar.size[0], avatar.size[1]), fill=255)
    avatar =  avatar.copy()
    avatar.putalpha(mask)

    if avatar.size[0] > avatar_size:
        avatar.thumbnail((avatar_size, avatar_size), Image.ANTIALIAS)
    else:
        avatar = avatar.resize((avatar_size, avatar_size), Image.ANTIALIAS)
    
    draw.ellipse([int((width-avatar_boundry)/ 2), 
        rectangle_top - (avatar_boundry/2), 
        int((width+avatar_boundry)/ 2) , 
        rectangle_top + (avatar_boundry/2)], 
        fill=(256,256,256))
    image.paste(avatar, (int((width-avatar_size)/ 2) , int(rectangle_top - (avatar_size/2))), mask=avatar)
    font = ImageFont.truetype("./fonts/Roboto-Black.ttf", name_font_size)
    w, h = draw.textsize(display_name, font=font)
    draw.text((int((width-w)/2),int(rectangle_top + avatar_boundry/2)), display_name, font=font, fill=(0,0,0))
    font = ImageFont.truetype("./fonts/Roboto-Bold.ttf", handle_font_size)
    w, h = draw.textsize(handle, font=font)
    draw.text((int((width-w)/2),int(rectangle_top + avatar_boundry/2 + 64)), handle, font=font, fill=(35,35,35))

    line_height = rectangle_top + (avatar_size /2) + name_font_size + handle_font_size 
    font = ImageFont.truetype("./fonts/Roboto-Regular.ttf", tweet_text_font_size)
    for line in lines:
        single_line_width, single_line_height = font.getsize(line)
        line_height += single_line_height + 5
        draw.text((130, line_height), line, font=font, fill=(55,55,55))

    return image

@click.command()
@click.option('-u', default ="", help="Paste url of the tweet")
@click.option('-s', default=False, help="flag for stream mode")
def url_2_story(u, s):
    """Create beautiful stories from tweets"""
    if(s) :
        user = api.lookup_users(screen_names=[s])[0]
        user = json.loads(json.dumps(user._json))
        print("streaming tweets for " + user['name'])
        stream_listener = TwitterStream()
        stream = tweepy.Stream(auth = api.auth, listener=stream_listener, tweet_mode="extended")
        stream.filter(follow=[user['id_str']])
    elif u!="":
        tweet = fetch_tweet_from_url(u)
        image = draw_story(tweet)
        save_story(image, name = tweet["user"]["screen_name"] + "_" + str(tweet["id"]))
    else:
        print("missing args")
    print(u)

if __name__ == '__main__':
    url_2_story()
