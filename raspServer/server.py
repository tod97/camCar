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
def moveMotors(dLeft, dRight):
    if dLeft > 0 and dRight > 0:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
    else:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
def stopMotors():
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
            

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
    stopMotors()
    GPIO.cleanup()
    pass
@sio.on('move')
def move(sid, data):
    print 'Left Power: ' + str(data['dLeft']) + ' Right Power: ' + str(data['dRight'])
    moveMotors(data['dLeft'], data['dRight'])
    pass
@sio.on('stopMove')
def stopMove(sid, data):
    print 'Stop moving.'
    stopMotors()
    pass

#MAIN EXECUTE
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)