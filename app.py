import os
import re
import facebook
import requests
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, escape
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

@app.route('/')
def hello():
	return render_template('index.html')
@app.route('/hearts')
def love():
	#token = request.cookies.get('fbsr_1441116782789661')
	print request.cookies
	user = facebook.get_user_from_cookie(request.cookies,'1441116782789661','608a6502fb85bbbe7e0cafabcaa8832e')
	print user
	#url = "https://graph.facebook.com/debug_token?input_token="+token+"&access_token={1441116782789661}"
	#r = requests.get(url)
	#print r.text
	#graph = facebook.GraphAPI(token)
	#profile = graph.get_object("me")
	#friends = graph.get_connections("me", "friends")
	#print friends
	return render_template('hearts.html')
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)