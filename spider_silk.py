
import sys

# acess to flask and sqlalchemy
sys.path.append('/home/rogue/.local/lib/python3.7/site-packages')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('Arachne')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///var/www/arachne/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(127))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer)
    pokemon = db.Column(db.String(20))

    def __repr__(self):
        return f'<Post {self.body}>'
