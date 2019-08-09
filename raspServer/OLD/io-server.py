import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print ('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('shortMove')
def another_event(sid, data):
    print 'Short moving: ' + data['position']
    pass

@sio.on('startMove')
def another_event(sid, data):
    print 'Start moving: ' + data['position']
    pass

@sio.on('stopMove')
def another_event(sid, data):
    print 'Stop moving.'
    pass

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

