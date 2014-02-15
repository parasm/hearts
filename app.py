import os
import re
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, escape
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

@app.route('/')
def hello():
	#email,read_mailbox,read_friendlists,friends_online_presence,user_online_presence&redirect_uri=http://www.facebook.com/connect/login_success.html
	return render_template('index.html')
@app.route('/2')
def test2():
	return render_template('index2.html')
@app.route('/')
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)