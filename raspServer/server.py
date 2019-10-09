import cv2
import eventlet
import socketio
import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response

#VIDEOCAMERA DEFINITION
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


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
sio.async_mode='threading'
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

#PY CAMERA API
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5005)), app)
