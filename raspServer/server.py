import eventlet
import socketio
import RPi.GPIO as GPIO
from time import sleep

#DC MOTORS CONFIG
Motor1A = 16
Motor1B = 18
Motor1E = 22
Motor2A = 19
Motor2B = 21
Motor2E = 23
def GPIOConfig():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    GPIO.setup(Motor2E,GPIO.OUT)
#DC MOTORS FUNCTIONS
def move(back, left, right):
    if back:
        if left:
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor1E,GPIO.HIGH)
        if right:
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            GPIO.output(Motor2E,GPIO.HIGH)
    else:
        if left:
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor1E,GPIO.HIGH)
        if right:
            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)
            GPIO.output(Motor2E,GPIO.HIGH)
def stopMotors(l = True, r = True):
    if l:
        GPIO.output(Motor1E,GPIO.LOW)
    if r:
        GPIO.output(Motor2E,GPIO.LOW)

def startMotors(position):
    if position == 'forward':
        move(False, True, True)
    if position == 'back':
        move(True, True, True)
    if position == 'left':
        move(False, True, False)
    if position == 'right':
        move(False, False, True)


#PY SOCKET CONFIG
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
#PY SOCKET EVENTS
@sio.event
def connect(sid, environ):
    GPIOConfig()
    pass
@sio.event
def disconnect(sid):
    GPIO.cleanup()
    pass
@sio.on('shortMove')
def shortMove(sid, data):
    print 'Short moving: ' + data['position']
    startMotors(data['position'])
    sleep(0.5)
    stopMotors()
    pass
@sio.on('startMove')
def startMove(sid, data):
    print 'Start moving: ' + data['position']
    startMotors(data['position'])
    pass
@sio.on('stopMove')
def stopMove(sid, data):
    print 'Stop moving.'
    stopMotors()
    pass

#MAIN EXECUTE
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)