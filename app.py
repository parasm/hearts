import os
import re
import facebook
import requests
from flask import Flask, render_template, request, session, redirect, escape
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

@app.route('/')
def hello():
	return render_template('index.html')
@app.route('/hearts')
def love():	
	user = facebook.get_user_from_cookie(request.cookies,'1441116782789661','608a6502fb85bbbe7e0cafabcaa8832e')
	token = user.get('access_token')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	inbox = graph.get_connections("me","inbox")
	name1 = [None,0]
	name2 = [None,0]
	messages = inbox.get('data')[0].get('comments').get('data')
	for x in messages:
		name = x.get('from').get('name')
		if not(name1[0]):
			name1[0] = name
		else:
			name1[1]+=1
		if not(name2[0]) or name1[0] != name:
			name2[0] = name
		else:
			name2[1]+=1
		print name
	print name1[0] + " count: " + str(name1[1])
	print name2[0] + " count: " + str(name2[1])
	return render_template('hearts.html')
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)