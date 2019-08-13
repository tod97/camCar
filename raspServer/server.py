import eventlet
import socketio
import RPi.GPIO as GPIO
from time import sleep

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

def turnMotors(angle):
    global rightPwm, leftPwm
    rightPwm.ChangeDutyCycle(100)
    leftPwm.ChangeDutyCycle(100)
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(0.0038 * angle)
    stopMotors()

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
    print 'Left Power: ' + str(int(data['dLeft'])) + ' Right Power: ' + str(int(data['dRight']))
    moveMotors(int(data['dLeft']), int(data['dRight']))
    pass
@sio.on('turn')
def turn(sid, data):
    print 'Turn ' + str(data['angle']) + ' degrees'
    turnMotors(data['angle'])
    pass
@sio.on('stopMove')
def stopMove(sid, data):
    print 'Stop moving.'
    stopMotors()
    pass

#MAIN EXECUTE
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)