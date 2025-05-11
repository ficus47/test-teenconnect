import json
import os
import shutil
from datetime import datetime

BASE_DIR = "data"
USER_DIR = os.path.join(BASE_DIR, "users")
POST_DIR = os.path.join(BASE_DIR, "posts")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")

os.makedirs(USER_DIR, exist_ok=True)
os.makedirs(POST_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def create_user(user_id, infos):
    user_file = os.path.join(USER_DIR, f"{user_id}.json")
    if os.path.exists(user_file):
        raise Exception("User already exists")

    user_data = {
        "name": infos.get("name", ""),
        "desc": infos.get("desc", ""),
        "list_post": [],
        "liked_post": [],
        "friends": [],
        "chat_id": [],
        "infos": infos.get("infos", {}),
        "settings": infos.get("settings", {})
    }
    save_json(user_file, user_data)

def create_post(user_id, desc, video_file_path):
    post_id = f"post_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
    video_target = os.path.join(VIDEO_DIR, f"{post_id}.mp4")
    shutil.copy(video_file_path, video_target)

    post_data = {
        "nb_like": 0,
        "nb_view": 0,
        "nb_comment": 0,
        "user_id": user_id,
        "content": video_target,
        "desc": desc,
        "comments": []
    }
    save_json(os.path.join(POST_DIR, f"{post_id}.json"), post_data)

    user_path = os.path.join(USER_DIR, f"{user_id}.json")
    user_data = load_json(user_path)
    user_data["list_post"].append(post_id)
    save_json(user_path, user_data)
    return post_id

def like_post(user_id, post_id):
    post_path = os.path.join(POST_DIR, f"{post_id}.json")
    post_data = load_json(post_path)
    post_data["nb_like"] += 1
    save_json(post_path, post_data)

    user_path = os.path.join(USER_DIR, f"{user_id}.json")
    user_data = load_json(user_path)
    if post_id not in user_data["liked_post"]:
        user_data["liked_post"].append(post_id)
    save_json(user_path, user_data)

def add_comment(post_id, user_id, comment):
    post_path = os.path.join(POST_DIR, f"{post_id}.json")
    post_data = load_json(post_path)
    post_data["nb_comment"] += 1
    post_data["comments"].append({
        "user": user_id,
        "comment": comment,
        "when": datetime.utcnow().isoformat()
    })
    save_json(post_path, post_data)

def get_user_profile(user_id):
    user_path = os.path.join(USER_DIR, f"{user_id}.json")
    return load_json(user_path)

def get_post(post_id):
    post_path = os.path.join(POST_DIR, f"{post_id}.json")
    return load_json(post_path)

def delete_post(user_id, post_id):
    post_path = os.path.join(POST_DIR, f"{post_id}.json")
    video_path = os.path.join(VIDEO_DIR, f"{post_id}.mp4")
    user_path = os.path.join(USER_DIR, f"{user_id}.json")

    if os.path.exists(post_path):
        os.remove(post_path)
    if os.path.exists(video_path):
        os.remove(video_path)

    user_data = load_json(user_path)
    user_data["list_post"] = [pid for pid in user_data["list_post"] if pid != post_id]
    save_json(user_path, user_data)

def add_friend(user_id, friend_id):
    user_path = os.path.join(USER_DIR, f"{user_id}.json")
    user_data = load_json(user_path)
    if friend_id not in user_data["friends"]:
        user_data["friends"].append(friend_id)
    save_json(user_path, user_data)
