import json
import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
import os 
import pathlib
import re
from sys import platform

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
font_url = "https://raw.githubusercontent.com/dilpreetsio/tweet2story/master/tweet2story/fonts/roboto.ttf"


def getOs():
    operating_system = ""
    if platform == "linux" or platform == "linux2":
        operating_system = "linux"
    elif platform == "darwin":
        operating_system = "mac"
    elif platform == "win32":
        operating_system = "windows"
    
    return operating_system


def getDesktopPath(operating_system):
    desktop =  ""
    if operating_system == "linux" or operating_system == "mac":
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    elif operating_system == "windows":
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    return desktop

# https://stackoverflow.com/a/49146722/330558
def removeEmoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def saveStory(image, desktop_path, name):
    image.save(os.path.join(desktop_path, name +".png"))

def drawStory(tweet, bg_color):
    desktop_path = getDesktopPath(getOs())
    response = requests.get(font_url)
    font_file = response.content

    tweet_text = removeEmoji(tweet["tweet"])
    display_name = tweet["display_name"]
    handle = "@" + tweet["handle"]
    avatar_url = tweet["avatar"]
    avatar_url = avatar_url[:avatar_url.rindex('_')] + avatar_url[avatar_url.rindex('.') :]
    response = requests.get(avatar_url)

    image = Image.new('RGBA', (1080, 1920), bg_color) #bg with twitter color
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(BytesIO(font_file), tweet_text_font_size)
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
    font = ImageFont.truetype(BytesIO(font_file), name_font_size)
    w, h = draw.textsize(display_name, font=font)
    draw.text((int((width-w)/2),int(rectangle_top + avatar_boundry/2)), display_name, font=font, fill=(0,0,0))
    font = ImageFont.truetype(BytesIO(font_file), handle_font_size)
    w, h = draw.textsize(handle, font=font)
    draw.text((int((width-w)/2),int(rectangle_top + avatar_boundry/2 + 64)), handle, font=font, fill=(35,35,35))

    line_height = rectangle_top + (avatar_size /2) + name_font_size + handle_font_size
    font = ImageFont.truetype(BytesIO(font_file), tweet_text_font_size)
    for line in lines:
        single_line_width, single_line_height = font.getsize(line)
        line_height += single_line_height + 5
        draw.text((int((width-tweet_text_width)/2), line_height), line, font=font, fill=(55,55,55))

    saveStory(image, desktop_path, name = tweet["handle"] + "_" + str(tweet["id"]))

    return "completed"