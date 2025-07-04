import requests
from datetime import datetime
import os
import csv

ACCESS_TOKEN = 'ENTER YOUR ACCESS TOKEN THAT YOU GET FROM DEVELOPERS.FACEBOOK'
IG_USER_ID = 'ENTER YOUR USER_ID NUMBER HERE(YOU CAN GET THIS FROM YOUR ACCOUNT ON INSTAGRAM)'
API_VERSION = 'v19.0'
BASE_URL = 'https://graph.facebook.com/v19.0'

def get_account_details():
    url = f"{BASE_URL}/{IG_USER_ID}?fields=followers_count,media_count,username,profile_picture_url,biography,name,website&access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    return {
        "name": response.get("name"),
        "username": response.get("username"),
        "followers": response.get("followers_count"),
        "posts": response.get("media_count"),
        "bio": response.get("biography"),
        "website": response.get("website"),
        "profile_pic": response.get("profile_picture_url")
    }

def get_recent_posts(limit=6):
    url = f"{BASE_URL}/{IG_USER_ID}/media?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,comments_count,like_count&limit={limit}&access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    return response.get("data", [])

def save_growth(follower_count, post_count):
    growth_file = "growth.csv"
    exists = os.path.exists(growth_file)
    with open(growth_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "follower_count", "post_count"])
        writer.writerow([datetime.now().isoformat(), follower_count, post_count])
