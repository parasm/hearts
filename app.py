from __future__ import division
import os
import re
import facebook
import json
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, escape, make_response
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

client = MongoClient("mongodb://parasm:slimreaper@troup.mongohq.com:10092/pretzels")
db = client.get_default_database()
chats = db.chats
counter = []
count_dict = {}

@app.route('/')
def hello():
	return render_template('index.html')
@app.route('/hearts')
def love():	
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
		if name1[0] == me:
			count_dict[name2[0]] = [name1[1],name2[1]]
		else:
			count_dict[name1[0]]= [name2[1],name1[1]]
		print name2[0] + " count: " + str(name2[1])
		counter.append(str(name2[0]) + " count: " + str(name2[1]))
		if name2[0] == me:
			count_dict[name1[0]] = [name2[1],name1[1]]
		else:
			count_dict[name2[0]] = [name1[1],name2[1]]
	#dict stores value of person chatting with, and maps to [your number,their number]
	print count_dict
	id = chats.insert({"chats":count_dict})
	resp = make_response(render_template('hearts.html', counter=counter, id=id))
	resp.set_cookie('id_code', str(id))
	return resp
@app.route('/find', methods=['GET','POST'])
def find():
	if request.method == 'POST':
		id_code = request.form.get('id')
		try:
			chat = chats.find({'_id':ObjectId(id_code)}).limit(1)[0]
		except Exception, e:
			print e
			return render_template('find.html', chat="could not find id")
		chat = json.dumps(chat.get('chats'))
		return chat
	return render_template('find.html')
@app.route('/stats')
def stats():
	names = []
	ratios = []
	ratios2 = []
	count = []
	num = 0
	for n in count_dict:
		names.append(n)
		count.append(num)
		you = count_dict.get(n)[0]
		them = count_dict.get(n)[1]
		ratios.append((you-them)/(you+them))
		ratios2.append((you/(you+them))*100)
		num+=1
	print ratios
	print names
	return render_template('stats.html', count=count, names=names, ratios=ratios, ratios2=ratios2)
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)