import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app) # Connects to the DB, dpeends DATABASE URL ENV.

from models import Result


@app.route('/')
def hello():
    return "Hello Development People"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    #print(os.environ['APP_SETTINGS']) # Sanity Check
    app.run()
    
