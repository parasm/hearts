from __future__ import division
import os
import ast
import re
import facebook
import json
import sendgrid
import requests
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, request, session, redirect, escape, make_response
import jinja2

app = Flask(__name__)
app.secret_key = 'paras_is_the_slim_reaper'

#who wants the D button, you pick gender etc. match %
#client = MongoClient("mongodb://parasm:slimreaper@troup.mongohq.com:10092/pretzels")
#db = client.get_default_database()
#chats = db.chats
s = sendgrid.Sendgrid('parasm', 'bcabooks', secure=True)
#counter = []
count_dict = {}
relationships_dict = {}
genders_dict = {}
friend_url = {}
words_per = {}
email_str = "<h1>Your conversation stats:</h1>"

def reset():
	global count_dict
	count_dict = {}
	global relationships_dict
	relationships_dict = {}
	global genders_dict
	genders_dict = {}
	global friend_url
	friend_url = {}

def reset_email():
	global email_str
	email_str = "<h1>Your conversation stats:</h1>"
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
	for w in data:
		if not(w.get('comments')):
			continue
		messages = w.get('comments').get('data')
		name1 = [None,0]
		name2 = [None,0]
		average_1 = 0
		average_2 = 0
		num_messages = 0
		num_messages_1 = 0
		num_messages_2 = 0
		for x in messages:
			if not(x.get('from')):
				continue
			name = x.get('from').get('name')
			if not(x.get('message')):
				continue
			message = x.get('message').split(' ')
			num_messages+=1
			if not(name1[0]):
				name1[0] = name
				name1[1] +=1
				average_1 += len(message)
				num_messages_1 += 1
			elif name1[0] == name:
				name1[1]+=1
				average_1 += len(message)
				num_messages_1 += 1
			if not(name2[0]) and name1[0] != name:
				name2[0] = name
				name2[1]+=1
				average_2 += len(message)
				num_messages_2 += 1
			elif name2[0] == name:
				name2[1] +=1
				average_2 += len(message)
				num_messages_2 += 1
		if num_messages_1 == 0:
			num_messages_1 = 1
		if num_messages_2 == 0:
			num_messages_2 = 1
		if name1[0] == me:
			count_dict[name2[0]] = [name1[1],name2[1]]
			words_per[name2[0]] = [average_1/num_messages_1,average_2/num_messages_2]
		else:
			count_dict[name1[0]]= [name2[1],name1[1]]
			words_per[name1[0]] = [average_2/num_messages_2,average_1/num_messages_1]
		if name2[0] == me:
			count_dict[name1[0]] = [name2[1],name1[1]]
			words_per[name1[0]] = [average_2/num_messages_2,average_1/num_messages_1]
		else:
			count_dict[name2[0]] = [name1[1],name2[1]]
			words_per[name2[0]] = [average_1/num_messages_1,average_2/num_messages_2]
	#dict stores value of person chatting with, and maps to [your number,their number]
	for f in count_dict:
		for friend in friends:
			if friend.get("name") == f:
				url = "https://graph.facebook.com/"+str(friend.get('id')+'?fields=gender,relationship_status,username&access_token=' + token)
				r = requests.get(url)
				r = r.text
				r = ast.literal_eval(r)
				genders_dict[f] = r.get("gender")
				friend_url[f] = "http://facebook.com/"+str(r.get('username'))
				relationships_dict[f] = r.get('relationship_status')

	return redirect('/stats')
@app.route('/stats', methods=['GET','POST'])
def stats():
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
		percents.append(round((you/(you+them))*100,2))
		avg_rounded = [round(words_per.get(n)[0],2),round(words_per.get(n)[1],2)]
		avg_words.append(avg_rounded)# you then them
		if n in count_dict:
			try:
				genders.append(str(genders_dict[n]))
			except KeyError, e:
				#we know its none
				genders.append(None)
			try:
				relationships.append(relationships_dict[n])
			except KeyError, e:
				#we know its none
				relationships.append(None)
			try:
				urls.append(friend_url[n])
			except KeyError, e:
				#we know its none
				urls.append(None)
		num+=1
	reset()
	reset_email()
	for x in count:
		if abs(50-percents[x]) <= 10: 
			try: 
				global email_str
				email_str += "<h2>Name:"+str(names[x])+"</h2>"
				if genders[x] != None:
					email_str += "<h3>  Gender: "+str(genders[x]) + "</h3>"
				if relationships[x] != None:
					email_str += "<h3>  Relationship Status: "+str(relationships[x]) + "</h3>"
				email_str += "<p>You send them " + str(avg_words[x][0])+" words per mesage.</p>"
				email_str += "<p>They send " + str(avg_words[x][1])+" words per message.</p>"
				email_str += "<p>You send "+str(percents[x])+"% of the chat messages."
			except Exception, e:
				continue
		else:
			continue
	return render_template('stats.html', count=count, names=names, percents=percents, relationships=relationships, genders=genders, urls=urls, avg_words=avg_words)
@app.route('/send', methods=['GET','POST'])
def send():
	if request.method == 'POST':
		email = request.form.get('email')
		message = sendgrid.Message("stats@gimmehearts.com", "Conversation Stats", "plaintext message body",
    			str(email_str))
		message.add_to(email,"User")
		s.web.send(message)
		reset_email()
	return redirect('/')
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
@app.route('/logout')
def logout():
	return render_template('logout.html')


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
