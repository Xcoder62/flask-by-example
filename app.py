import os
import operator
import re
import nltk
import requests
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) # Connects to the DB, dpeends DATABASE URL ENV.

from models import Result


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    
    if request.method == "POST":
        # Get URL from user
        try:
            url = request.form['url']
            r = requests.get(url)
            #print(r.text) prints all of the site's html in the console
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid, then try again."
            )
            return render_template('index.html', errors=errors)
        if r:
            # text processing
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            nltk.data.path.append('./nltk_data/') # set path
            tokens = nltk.word_tokenize(raw) # converts text into words
            text = nltk.Text(tokens) # convert to a list of words
            
            # remove punctation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            
            # Stop Words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)

            # Save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )[:10] #remove for all results instead of top 10
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to DB.")
    return render_template('index.html', errors=errors, results=results)

# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

if __name__ == '__main__':
    #print(os.environ['APP_SETTINGS']) # Sanity Check
    app.run()
    
