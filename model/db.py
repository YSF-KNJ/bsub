import sqlite3
from utils import helpers
from datetime import datetime

def execute_query(query, args=()):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    conn.commit()
    cursor.close()
    conn.close()

def create_tables():
    execute_query('''
        CREATE TABLE IF NOT EXISTS creator (
            creator_id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_name TEXT,
            creator_email TEXT,
            whatsapp_number TEXT,
            solde REAL,
            password TEXT)''')
    execute_query('''
        CREATE TABLE IF NOT EXISTS video (
            video_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ytp_id TEXT,
            thumbnail_url TEXT,
            video_length REAL,
            video_price REAL,
            video_date DATE,
            video_status TEXT,
            creator_id INTEGER,
            translation_file TEXT,
            FOREIGN KEY (creator_id) REFERENCES creator(creator_id))''')

def get_solde(creator_id):
    conn = sqlite3.connect('bsub.db')
    cursor = conn.cursor()
    cursor.execute('SELECT solde FROM creator WHERE creator_id = ?', (creator_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(result[0])

def is_added(price,creator_id):
    if get_solde(creator_id) >= video_price:
        return True
    else:
        return False

def add_video(url,creator_id):    
    ytp_id = helpers.video_id(url)
    thumbnail_url = helpers.video_thumbnail(url)
    video_length = helpers.video_length(url)
    video_price = helpers.video_price(url)
    video_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    video_status = "added"

    execute_query('''
    INSERT INTO video (ytp_id, thumbnail_url, video_length, video_price, video_date, video_status, creator_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (ytp_id, thumbnail_url, video_length, video_price, video_date, video_status, creator_id))

def is_deleted(video_id):
    conn = sqlite3.connect('bsub.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM video WHERE video_id = ?',(video_id,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if result == 'added':
        return True
    else:
        return False

def delete_video(video_id):
    if is_deleted(video_id):
        execute_query('DELETE FROM video WHERE video_id = ?', (video_id,))

def add_creator(creator_name,creator_email,password,whatsapp_number):
    execute_query('''
    INSERT INTO creator (creator_name, creator_email, whatsapp_number, solde, password)
    VALUES (?, ?, ?, ?, ?)''',
    (creator_name, creator_email, whatsapp_number, 0, password))
    conn.commit()

def get_pass(email):
    connection = sqlite3.connect('bsub.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password FROM creator WHERE creator_email = ?', (email,))
    password = cursor.fetchone()
    cursor.close()
    connection.close()
    if password == None:
        return False
    else:
        return str(password[0])

def get_id(email):
    connection = sqlite3.connect('bsub.db')
    cursor = connection.cursor()
    cursor.execute('SELECT creator_id FROM creator WHERE creator_email = ?', (email,))
    id = cursor.fetchone()
    cursor.close()
    connection.close()
    return id[0]

def get_videos(creator_id):
    conn = sqlite3.connect('bsub.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM video WHERE creator_id = ?', (creator_id,))
    videos = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return videos

def change_password(email,new_password):
    execute_query("UPDATE creator SET password = ? WHERE creator_email = ?",(new_password,email))
