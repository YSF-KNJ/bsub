def video_id(url: str) -> str:
    import re
    regex = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11})")
    match = regex.search(url)
    if match:
        return match.group(1)
    else:
        return None

def video_length(video_url):
    from pytube import YouTube
    video_url = 'https://youtu.be/' + video_id(video_url)
    try:
        yt = YouTube(video_url)
        length = yt.length
        return length
    except Exception:
        return None

def video_price(video_link,fac=0.125):
    from math import floor
    return floor(float(video_length(video_link))*fac)

def video_thumbnail(video_url):
    from pytube import YouTube
    video_url = 'https://youtu.be/' + video_id(video_url)
    try:
        yt = YouTube(video_url)
        thumbnail_url = yt.thumbnail_url
        return thumbnail_url
    except Exception:
        return None

def hash_md5(password):
    import hashlib
    md5_hash = hashlib.md5(password.encode())
    hashed_password = md5_hash.hexdigest()
    return str(hashed_password)

def generate_otp():
    from random import randint
    return f"{randint(0, 999999):06d}"

def send_email(subject, sender, recipients, body):
    from flask_mail import Mail, Message
    from app import app
    mail = Mail()
    with app.app_context():
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = body
        mail.send(msg)
