from flask import Blueprint, render_template, jsonify, request
from services.instagram_api import get_account_details, get_recent_posts, save_growth
from services.file_utils import download_file
import os
import csv

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return render_template('home.html')

@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('index.html')

@dashboard_bp.route('/dashboard/data')
def dashboard_data():
    account_data = get_account_details()
    save_growth(account_data["followers"], account_data["posts"])
    return render_template('index.html', account_data=account_data)

@dashboard_bp.route('/api/instagram/stats')
def instagram_stats():
    account = get_account_details()
    posts = get_recent_posts()
    return jsonify({"account": account, "recent_posts": posts})

@dashboard_bp.route('/api/instagram/download', methods=['POST'])
def download_media():
    data = request.get_json()
    path = download_file(data.get("media_url"), f"{data.get('post_id')}.jpg")
    return jsonify({"success": True, "filepath": path}) if path else jsonify({"success": False}), 500

@dashboard_bp.route('/api/instagram/export')
def export_csv():
    posts = get_recent_posts()
    filepath = os.path.join("data", "media.csv")
    os.makedirs("data", exist_ok=True)
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "caption", "likes", "comments", "url"])
        for post in posts:
            writer.writerow([
                post.get("id"), post.get("caption", ""), post.get("like_count", 0),
                post.get("comments_count", 0), post.get("media_url")
            ])
    return jsonify({"success": True, "filepath": filepath})

@dashboard_bp.route("/api/save_growth", methods=["POST"])
def api_save_growth():
    details = get_account_details()
    save_growth(details["followers"], details["posts"])
    return jsonify({"message": "Growth saved successfully."})
