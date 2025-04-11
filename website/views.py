from datetime import datetime, timedelta, timezone
import json
from flask import Blueprint, render_template, url_for, redirect, request
import os

import markdown

def files_as_dict(directory):
    files = os.listdir(directory)
    files_with_ctime = [(os.path.join(directory, file), os.path.getctime(os.path.join(directory, file))) for file in files]
    files_sorted = sorted(files_with_ctime, key=lambda x: x[1])
    result_dict = {i + 1: file[0] for i, file in enumerate(files_sorted)}
    return result_dict

blogs = files_as_dict("website/blogs/")
json_album_files = files_as_dict('website/albums/')

views = Blueprint("views", __name__)

def get_duration_since_2007():
    start_time = datetime(2007, 9, 5, 1, 0, 0)
    now = datetime.now()

    # Get total duration
    delta = now - start_time

    # Break into components
    total_seconds = int(delta.total_seconds())
    seconds = total_seconds % 60
    minutes = (total_seconds // 60) % 60
    hours = (total_seconds // 3600) % 24
    days_total = delta.days

    years = days_total // 365
    months = (days_total % 365) // 30
    days = (days_total % 365) % 30

    return f"{years:02}:{months:02}:{days:02}:{hours:02}:{minutes:02}:{seconds:02}"

@views.route("/")
def home():
    utc_plus_6 = timezone(timedelta(hours=6))
    current_time = datetime.now(utc_plus_6).strftime("%Y:%m:%d %H:%M:%S%z")

    # Insert colon in timezone offset to match "+06:00"
    formatted_time = current_time[:-2] + ':' + current_time[-2:]
    print(request.remote_addr)
    return render_template("index.html", blogs=blogs, current_date=formatted_time, duration=get_duration_since_2007())

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")

@views.route("/blog")
def blog():
    b_num = request.args.get("b")
    if b_num:
        blog_filepath = blogs[int(b_num)]
        with open(blog_filepath, 'r') as f:
            html_content = markdown.markdown(f.read(), extensions=['fenced_code'])
        return render_template("base_blog.html", blog_content=html_content)
    
@views.route("/alp")
def alp():
    return render_template("albums.html", json_albums=json_album_files)
    

@views.route("/album")
def album():
    album_arg = request.args.get("a")
    if album_arg:
        al_filepath = json_album_files[int(album_arg)]
        with open(al_filepath, 'r') as f:
            json_data = json.load(f)
            print(json_data)
            return render_template("album.html", al=json_data)