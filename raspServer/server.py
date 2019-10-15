from threading import Thread, Lock
import cv2
import eventlet
import socketio
import threading
import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response

#VIDEOCAMERA DEFINITION
class CameraStream(object):
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)

        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()

cap = CameraStream().start()


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
app = Flask(__name__)

#PY CAMERA API
@app.route('/')
def index():
    return render_template('index.html')


def gen_frame():
    while cap:
        frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(),
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
def serve_app(_sio, _app):
    app = socketio.Middleware(_sio, _app)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
    
#MAIN EXECUTE
if __name__ == '__main__':
    
    wst = threading.Thread(target=serve_app, args=(sio,app))
    wst.daemon = True
    wst.start()
