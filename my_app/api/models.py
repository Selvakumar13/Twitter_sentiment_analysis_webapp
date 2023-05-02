from my_app import db
from flask_login import UserMixin

class Hash(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    hashtag = db.Column(db.String(255))
    tweets=db.relationship('Tweet',backref='hash',lazy=True)
    def __repr__(self):
        return f'User{self.name}{self.hashtag}'

class Tweet(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(255))
    hash_id=db.Column(db.Integer,db.ForeignKey('hash.id'), nullable=False)
    def __repr__(self):
        return f'Task{self.text}'

class Output(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    output=db.Column(db.String(255))
            
    def __repr__(self):
        return f'Task{self.output}'
    
    