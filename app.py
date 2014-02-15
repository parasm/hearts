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
	counter = []
	count_dict = {}
	user = facebook.get_user_from_cookie(request.cookies,'1441116782789661','608a6502fb85bbbe7e0cafabcaa8832e')
	token = user.get('access_token')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	me = profile.get('first_name') +" "+ profile.get('last_name')
	inbox = graph.get_connections("me","inbox")
	data = inbox.get('data')
	for w in data:
		try:
			messages = w.get('comments').get('data')
		except AttributeError, e:
			break
		name1 = [None,0]
		name2 = [None,0]
		for x in messages:
			name = x.get('from').get('name')
			if not(name1[0]):
				name1[0] = name
				name1[1] +=1
			elif name1[0] == name:
				name1[1]+=1

			if not(name2[0]) and name1[0] != name:
				name2[0] = name
				name2[1]+=1
			elif name2[0] == name:
				name2[1] +=1
		print name1[0] + " count: " + str(name1[1])
		counter.append(str(name1[0]) + " count: " + str(name1[1]))
		count_dict[name1[0]] = name1[1]
		print name2[0] + " count: " + str(name2[1])
		counter.append(str(name2[0]) + " count: " + str(name2[1]))
		count_dict[name2[0]] = name2[1]
	print count_dict
	return render_template('hearts.html', counter=counter)
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)