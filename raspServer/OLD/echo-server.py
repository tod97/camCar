from flask import Flask, render_template
from flask_socketio import send, SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    print 'Client connected'

@socketio.on('message')
def handle_message(message):
    print 'received message: ' + message
    send(message)

@socketio.on('json')
def handle_json(json):
    print 'received json: ' + str(json)
    send(json)

@socketio.on('move')
def moveEvent(json):
    print 'received move: ' + str(json)
    send(json)




if __name__ == '__main__':
    socketio.init_app(app, cors_allowed_origins="*")
    socketio.run(app,'0.0.0.0')