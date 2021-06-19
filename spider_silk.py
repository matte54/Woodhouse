
import sys

# acess to flask and sqlalchemy
sys.path.append('/home/rogue/.local/lib/python3.7/site-packages')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('Arachne')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/arachne/app.db'
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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # db id
    trainer_id = db.Column(db.Integer, unique=True)  # discord id
    # make names require a minimum length
    name = db.Column(db.String(40), index=True, unique=True)  # display name
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.Column(db.DateTime, default=datetime.utcnow)
    favorite = db.Column(db.String(20))
    bio = db.Column(db.String(255))
    color = db.Column(db.String(7))
    avatar = db.Column(db.String(63))

    def __repr__(self):
        return f'<User {self.name}>'

def check_new_user(name=None, trainer_id=None):
    if not name or not trainer_id:
        print(f'invalid username: {name} or id: {trainer_id}')
        return
    query = User.query.filter_by(trainer_id=trainer_id).all()
    if not query:
        u = User(name=name, trainer_id=trainer_id)
        db.session.add(u)
        db.session.commit()
        print(f'added new user {name} to database')
        return
        
