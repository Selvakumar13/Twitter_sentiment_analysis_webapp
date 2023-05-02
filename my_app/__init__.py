from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators

SECRET_KEY='some secret key'
app=Flask(__name__)
app.config['SECRET_KEY']=SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///C:/Users/DELL/twtsa/my_app/twts_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

with app.app_context():
    db.create_all()
        
from my_app.api.views import twt
app.register_blueprint(twt)

