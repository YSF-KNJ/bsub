from flask import Flask
from flask_mail import Mail, Message


app = Flask(__name__,template_folder='../templates',static_folder='../static')

from app import views,admin_views

from model import db
db.create_tables()


app.secret_key = ''
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''

mail = Mail()
mail.init_app(app)