from flask import flash,redirect,render_template,request,jsonify,Blueprint,abort
from werkzeug.security import generate_password_hash,check_password_hash
from my_app import db
from my_app.api.models import Hash,Output,Tweet
from my_app.api.forms import Mainform
from flask import jsonify
import pickle
from flask import current_app
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import tweepy

#Intialising Tweepy with Twitter API Credentials
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAIqjnAEAAAAA6%2F9K3qhwxdhBWYixj5cYajmect4%3DrzxC8MhOkIUTMI5A8lGvsAxnVweNWoKQWw7WOYfFpr9gXLRRNf')



#setting the blueprint
twt=Blueprint('twts',__name__)

#Hompage
@twt.route('/',methods=['POST','GET'])
@twt.route('/home',methods=['POST','GET'])
def home():
    form=Mainform()
    if request.method=='GET':
        return render_template('sentiment.html', form=form)
    
    
    if request.method=='POST':
        if form.validate_on_submit:
            hasht=Hash(name=form.name.data,
                       hashtag=form.hashtag.data)
            db.session.add(hasht)
            db.session.commit()
    #Retrieve tweets for the hashtag
            hashtag=request.form['hashtag']
            tweets= client.search_all_tweets(query=hashtag,lang='en',max_results=2)
            tweet_texts=[tweet.text for tweet in tweets]
            
    
    # Store tweets in the database
            for tweet_text in tweet_texts:
                tweet=Tweet(text=tweet_text,hash=hasht)
                db.session.add(tweet)
            
    
    #Analyse sentiments using NLTK
            hashtag = request.form['hashtag']   
            sid = SentimentIntensityAnalyzer()
            scores = [sid.polarity_scores(tweet) for tweet in tweet_texts]
            avg_score=sum([score['compound'] for score in scores])/len(scores)
            
            if(avg_score > 0):
                label = 'This sentence is positive'
            elif(avg_score == 0):
                label = 'This sentence is neutral'
            else:
                label = 'This sentence is negative'
            outpt=Output(output=label)
            db.session.add(outpt)
            db.session.commit()
            return(render_template('prediction.html',sentiment=label))

        
@twt.route('/info')
def hashs():
    hasht=Hash.query.all()
    twet=Tweet.query.all() 
    outpt=Output.query.all()
    response = []
    for hashs,twets,outpts in zip(hasht,twet,outpt):
        hash_dict = {
            'name': hashs.name,
            'Hashtag': hashs.hashtag,
            'Hash_id': hashs.id,
            'Text': twets.text,
            'Output':outpts.output
            }

        response.append(hash_dict)
    return jsonify(response)
        
