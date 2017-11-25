from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect, send
# from __future__ import print_function
# import pymysql
from subprocess import call
from urlparse import urlparse
import socketio
from socketio import Middleware
import requests
import eventlet
import eventlet.wsgi
eventlet.monkey_patch()

app = Flask(__name__)
# sio = SocketIO( app, async_handlers=True)

sio = socketio.Server()

# app = Flask(__name__)
app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'

users = []
connections = []
dic = {}
url = 'http://crow.cs.illinois.edu:5000/'

@app.route( '/' )
def hello():
  return render_template( './ChatApp.html' )

# @app.route('/', methods=['POST'])
# def public_data():
#     return flask.Response("foo" * 10, mimetype='text/plain')

@sio.on('connect')
def on_connect(sid, environ):
	print("connect ", sid) 
	sio.emit('hello', 'yes')

@sio.on('disconnect')
def on_disconnect(sid):
	# username = data['username']
	# domain = data['domain_name']
	print(' left the game!')
	# leave_room(domain)
	# send(username + ' has left your domain', room=domain)
	# sio.emit('leave domain', 'You left ' + domain + 'successfully!', room=sid)
	# for x in users:
	# 	if x == username:
	# 		users.remove(x)
	# sio.emit('get users', users, room=domain)

@sio.on( 'my event' )
def handle_my_custom_event(sid, json):
  print( 'recived my event: ' + str( json ) ) #user is the sid
  print ('current user id is: ' + sid)
  sio.emit( 'my response', json, callback=messageRecived )

@sio.on('join')
def on_join(sid, data):
	currentsid = sid
	username = data['username']
	domain = data['domain_name']
	join_room(domain)
	send(username + ' has entered your domain', room=domain)
	sio.emit('enter domain', 'You entered ' + domain + 'successfully!', room=sid)


@sio.on('leave')	
def on_leave(sid, data):
	username = data['username']
	domain = data['domain_name']
	print(username + ' left the game!')
	# leave_room(domain)
	# send(username + ' has left your domain', room=domain)
	# sio.emit('leave domain', 'You left ' + domain + 'successfully!', room=sid)
	for x in users:
		if x == username:
			users.remove(x)
	sio.emit('get users', users, room=domain)

@sio.on( 'change domain' )
def change_domain(sid, data): 
	currentsid = sid
	username = data['username']	
	newdomain = data['domain_name']
	olddomain = dic[sid]
	dic[sid] = newdomain
	leave_room(olddomain)
	join_room(newdomain)
	send(username + ' has entered your domain', room=newdomain)
	sio.emit('new domain', 'You entered ' + newdomain + ' successfully!', room=sid)

def print_url(r, *args, **kwargs):
	print('Query recieved!')

def print_url_desc(r, *args, **kwargs):
	print('Query Description recieved!')

def calllib(domain, message):
	payload = {'url': domain, 'query': message}
	r = requests.get(url, allow_redirects=False, hooks={'response': print_url}, params=payload)
	return r

# @sio.on('send message')
# def send_message(sid, data):
# 	username = data['username']
# 	message = data['message']
# 	message = urlparse(message)
# 	domain = dic[sid]
# 	payload = {'url': domain, 'query': message}
# 	r = requests.get(url, hooks={'response': print_url}, params=payload)
# 	sio.emit('new message', {'msg': r.text, 'users': username}, room=domain)

@sio.on('send message by desc')
def send_message_by_desc(sid, data):
	username = data['username']
	message = data['message']
	message = urlparse(message)
	domain = dic[sid]
	payload_desc = {'url': domain, 'querydesc': message}
	r = requests.get(url, hooks={'response': print_url_desc}, params=payload_desc)
	for key in dic:
		if dic[key] == domain:
			sio.emit('new message', {'msg': r.text, 'users': username}, room=key)

	# sio.emit('new message', {'msg': r.text, 'users': username}, room=domain)

@sio.on('send message')
def send_message(sid, data):
	username = data['username']
	message = data['message']
	domain = dic[sid]
	for key in dic:
		if dic[key] == domain:
			sio.emit('new message', {'msg': message, 'users': username}, room=key)
	
@sio.on('new user')
def new_user(sid, data):
	currentsid = sid
	username = data['username']	
	users.append(username);
	domain = data['domain_name']
	dic[sid] = domain
	print(sid);
	# join_room(domain)
	# send(username + ' has entered your domain', room=domain)
	# sio.emit('get users', users, room=domain)
	for key in dic:
		if dic[key] == domain:
			sio.emit('get users', users, room=key)
	# sio.emit('get users', users, room=sid)


if __name__ == '__main__':
	app = socketio.Middleware(sio, app)
    # deploy as an eventlet WSGI server
	# eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5353)), app)
	# eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('127.0.0.1', 5353)), certfile='cert.crt',keyfile='private.key',server_side=True), app)
	eventlet.wsgi.server(eventlet.listen(('127.0.1.1', 5353)), app)
	eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('127.0.1.1', 5353)), certfile='cert.crt',keyfile='private.key',server_side=True), app)
	# sio.run(app, debug=True, host="0.0.0.0", port=5353)
	# sio.run(app, debug=True, port=5353)
