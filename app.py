from __future__ import division
import os
import ast
import re
import facebook
import json
#import sendgrid
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, escape, make_response
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

#client = MongoClient("mongodb://parasm:slimreaper@troup.mongohq.com:10092/pretzels")
#db = client.get_default_database()
#chats = db.chats
#s = sendgrid.Sendgrid('parasm', 'bcabooks', secure=True)
last_user =""
counter = []
count_dict = {}
relationships_dict = {}
genders_dict = {}
friend_url = {}
words_per = {}

def reset():
	counter = []
	count_dict = {}
	relationships_dict = {}
	genders_dict = {}
	friend_url = {}
	last_user=""

@app.route('/')
def hello():
	return render_template('index.html')
@app.route('/hearts')
def love():
	user = facebook.get_user_from_cookie(request.cookies,'1441116782789661','608a6502fb85bbbe7e0cafabcaa8832e')
	try:
		token = user.get('access_token')
	except AttributeError, e:
		return redirect('/')
	graph = facebook.GraphAPI(token)
	profile = graph.get_object("me")
	me = profile.get('first_name') +" "+ profile.get('last_name')
	inbox = graph.get_connections("me","inbox")
	data = inbox.get('data')
	friends = graph.get_connections("me","friends")
	friends = friends.get('data')
	#messaged_friends_names = []
	for w in data:
		if w.get("comments") is None:
			print w
		messages = w.get('comments').get('data')
		name1 = [None,0]
		name2 = [None,0]
		average_1 = 0
		average_2 = 0
		num_messages = 0
		for x in messages:
			name = x.get('from').get('name')
			message = x.get('message').split(' ')
			num_messages+=1
			#print str(message) + "avg: " +str(average)
			#print average
			if not(name1[0]):
				name1[0] = name
				name1[1] +=1
				average_1 += len(message)
			elif name1[0] == name:
				name1[1]+=1
				average_1 += len(message)
			if not(name2[0]) and name1[0] != name:
				name2[0] = name
				name2[1]+=1
				average_2 += len(message)
			elif name2[0] == name:
				name2[1] +=1
				average_2 += len(message)
		#print('swerve diff chat')
		#print name1[0] + " count: " + str(name1[1])
		counter.append(str(name1[0]) + " count: " + str(name1[1]))
		if name1[0] == me:
			count_dict[name2[0]] = [name1[1],name2[1]]
			words_per[name2[0]] = [average_1/num_messages,average_2/num_messages]
		else:
			count_dict[name1[0]]= [name2[1],name1[1]]
			words_per[name1[0]] = [average_2/num_messages,average_1/num_messages]
		#print name2[0] + " count: " + str(name2[1])
		counter.append(str(name2[0]) + " count: " + str(name2[1]))
		if name2[0] == me:
			count_dict[name1[0]] = [name2[1],name1[1]]
			words_per[name1[0]] = [average_2/num_messages,average_1/num_messages]
		else:
			count_dict[name2[0]] = [name1[1],name2[1]]
			words_per[name2[0]] = [average_1/num_messages,average_2/num_messages]
	#dict stores value of person chatting with, and maps to [your number,their number]
	print words_per
	for f in count_dict:#messaged_friends_names:
		for friend in friends:
			if friend.get("name") == f:
				url = "https://graph.facebook.com/"+str(friend.get('id')+'?fields=gender,relationship_status,username&access_token=' + token)
				#print str(friend.get('id'))
				r = requests.get(url)
				r = r.text
				#print r
				r = ast.literal_eval(r)
				#print r
				genders_dict[f] = r.get("gender")
				friend_url[f] = "http://facebook.com/"+str(r.get('username'))
				#print r.get('relationship_status')
				relationships_dict[f] = r.get('relationship_status')

	#print messaged_friends_names
	#print friends
	#print genders_dict
	#id = chats.insert({"chats":count_dict})
	#resp = make_response(render_template('hearts.html', counter=counter, id=id))
	#resp.set_cookie('id_code', str(id))
	#return resp
	return render_template('hearts.html', counter=counter)
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
@app.route('/stats', methods=['GET','POST'])
def stats():
	#if request.method == 'POST':
	#	to_email = request.form.get('email')
	#	message = sendgrid.Message("stats@gimmehearts.com", "Conversation stats","plaintext message body",
	#		"<h1>name</h1>")
	names = []
	percents = []
	count = []
	genders = []
	relationships = []
	urls = []
	avg_words = []
	num = 0
	for n in count_dict:
		names.append(n)
		count.append(num)
		you = count_dict.get(n)[0]
		them = count_dict.get(n)[1]
		percents.append((you/(you+them))*100)
		avg_words.append(words_per.get(n))# you then them
		if n in count_dict:
			genders.append(genders_dict[n])
			relationships.append(relationships_dict[n])
			urls.append(friend_url[n])
		num+=1
	return render_template('stats.html', count=count, names=names, percents=percents, relationships=relationships, genders=genders, urls=urls, avg_words=avg_words)
@app.errorhandler(404)
def broken(error):
	reset()
	return render_template('404.html'), 404

@app.errorhandler(500)
def broken(error):
	reset()
	return render_template('500.html'), 500
if __name__ == '__main__':

	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)