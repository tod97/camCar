import eventlet
import socketio
import RPi.GPIO as GPIO
from time import sleep
import datetime
import os

file_txt = None

#DC MOTORS CONFIG
Motor1A = 19
Motor1B = 21
Motor1E = 23
Motor2A = 16
Motor2B = 18
Motor2E = 22
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
rightPwm = GPIO.PWM(Motor1E, 100)
rightPwm.start(0)
leftPwm = GPIO.PWM(Motor2E, 100)
leftPwm.start(0)

#DC MOTORS FUNCTIONS
def moveMotors(dLeft, dRight):
    global rightPwm, leftPwm
    rightPwm.ChangeDutyCycle(abs(dRight))
    leftPwm.ChangeDutyCycle(abs(dLeft))
    if dLeft > 0 and dRight > 0:
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor1B,GPIO.LOW)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        GPIO.output(Motor2B,GPIO.LOW)
        GPIO.output(Motor2E,GPIO.HIGH)
    else:
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor1B,GPIO.HIGH)
        GPIO.output(Motor1E,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        GPIO.output(Motor2B,GPIO.HIGH)
        GPIO.output(Motor2E,GPIO.HIGH)

def stopMotors():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)


#PY SOCKET CONFIG
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
#PY SOCKET EVENTS
@sio.event
def connect(sid, environ):
    pass
@sio.event
def disconnect(sid):
    stopMotors()
    pass
@sio.on('move')
def move(sid, data):
    global file_txt
    if file_txt is not None:
        file_txt.write('Left Power: ' + str(int(data['dLeft'])) + ' Right Power: ' + str(int(data['dRight'])) + '\n')
    moveMotors(int(data['dLeft']), int(data['dRight']))
    pass
@sio.on('stopMove')
def stopMove(sid):
    print 'Stop moving.'
    stopMotors()
    pass

@sio.on('startRecord')
def startRecord(sid):
    global file_txt
    FILE_OUTPUT = os.path.join(os.path.expanduser('~'), 'records', str(datetime.datetime.now())+'.txt')
    file_txt = open(FILE_OUTPUT,"a")
    pass
@sio.on('stopRecord')
def stopRecord(sid, data):
    global file_txt
    file_txt.close()
    file_txt = None
    pass

#MAIN EXECUTE
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
