from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
# from __future__ import print_function
# import pymysql
from subprocess import call
from urlparse import urlparse
import requests
import grequests
# https://flask-socketio.readthedocs.io/en/latest/
# https://github.com/socketio/socket.io-client
url = 'http://crow.cs.illinois.edu:5000/'
app = Flask(__name__)

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'

socketio = SocketIO( app )
users = []
connections = []
dic = {}


@app.route( '/' )
def hello():
  return render_template( './ChatApp.html' )

def messageRecived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) ) #user is the request.sid
  print ('current user id is: ' + request.sid)
  socketio.emit( 'my response', json, callback=messageRecived )

@socketio.on('join')
def on_join(data):
	username = data['username']
	domain = data['domain_name']
	join_room(domain)
	send(username + ' has entered your domain', room=domain)
	emit('enter domain', 'You entered ' + domain + 'successfully!', room=request.sid)


@socketio.on('leave')	
def on_leave(data):
	username = data['username']
	domain = data['domain_name']
	# leave_room(domain)
	# send(username + ' has left your domain', room=domain)
	# emit('leave domain', 'You left ' + domain + 'successfully!', room=request.sid)
	for x in users:
		if x == username:
			users.remove(x)
	emit('get users', users, room=domain)

@socketio.on( 'change domain' )
def change_domain(data): 
	username = data['username']	
	newdomain = data['domain_name']
	olddomain = dic[request.sid]
	dic[request.sid] = newdomain
	leave_room(olddomain)
	join_room(newdomain)
	send(username + ' has entered your domain', room=newdomain)
	emit('new domain', 'You entered ' + newdomain + ' successfully!', room=request.sid)

def print_url(r, *args, **kwargs):
	print('Query recieved!')

def print_url_desc(r, *args, **kwargs):
	print('Query Description recieved!')

def calllib(domain, message):
	payload = {'url': domain, 'query': message}
	r = requests.get(url, allow_redirects=False, hooks={'response': print_url}, params=payload)
	return r

# @socketio.on('send message')
# def send_message(data):
# 	username = data['username']
# 	message = data['message']
# 	message = urlparse(message)
# 	domain = dic[request.sid]
# 	payload = {'url': domain, 'query': message}
# 	r = requests.get(url, hooks={'response': print_url}, params=payload)
# 	emit('new message', {'msg': r.text, 'users': username}, room=domain)

@socketio.on('send message by desc')
def send_message_by_desc(data):
	username = data['username']
	message = data['message']
	message = urlparse(message)
	domain = dic[request.sid]
	payload_desc = {'url': domain, 'querydesc': message}
	r = requests.get(url, hooks={'response': print_url_desc}, params=payload_desc)
	emit('new message', {'msg': r.text, 'users': username}, room=domain)

@socketio.on('send message')
def send_message(data):
	username = data['username']
	message = data['message']
	domain = dic[request.sid]
	emit('new message', {'msg': message, 'users': username}, room=domain)

@socketio.on('new user')
def new_user(data):
	username = data['username']
	users.append(username);
	domain = data['domain_name']
	dic[request.sid] = domain

	join_room(domain)
	send(username + ' has entered your domain', room=domain)
	emit('get domains', domain, room=request.sid)
	emit('get users', users, room=domain)


if __name__ == '__main__':
	socketio.run(app, debug=True, host="0.0.0.0", port=5353)
	# socketio.run(app, debug=True)