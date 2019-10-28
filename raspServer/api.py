from threading import Thread, Lock
import cv2
from flask import Flask, request, render_template, Response, jsonify
from flask_cors import CORS
import datetime
import json
import os
from os import listdir
from os.path import isfile, join

#VIDEOCAMERA DEFINITION
class CameraStream(object):
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)

        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.isRecording = False
        self.read_lock = Lock()

    def getWidth(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
    def getHeight(self):
        return self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    def getFrame(self):
        return self.stream.get(cv2.CAP_PROP_FPS)
    def startRecord(self):
        FILE_OUTPUT = os.path.join(os.path.expanduser('~'), 'records', str(datetime.datetime.now())+'.avi')
        width = cap.getWidth()
        height = cap.getHeight()
        frame = cap.getFrame()
        fourcc = cv2.VideoWriter_fourcc(*'X264')
        self.out = cv2.VideoWriter(FILE_OUTPUT,fourcc, frame, (int(width),int(height)))
        self.isRecording = True
    def stopRecord(self):
        self.isRecording = False
        self.out = None

    def startStream(self):
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
            if self.isRecording:
                self.out.write(frame)
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stopStream(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()

cap = CameraStream().startStream()
app = Flask(__name__)
CORS(app)

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

@app.route('/record',methods=['POST'])
def record():
    global cap
    request.get_data()
    data = json.loads(request.data)
    try:
        recordVideo = str(data['recordVideo'])
    except KeyError:
        return "Missing data", 500

    if recordVideo == "True":
        cap.startRecord()
        return "Start recording", 200
    else:
        cap.stopRecord()
        return "Stop recording", 200

@app.route('/record/delete',methods=['POST'])
def deleteRecord():
    data = json.loads(request.data)
    try:
        name = str(data['name'])
    except KeyError:
        return "Invalid name", 500
    path = os.path.join(os.path.expanduser('~'), 'records', name)
    os.remove(path)
    return "File removed", 200

@app.route('/records',methods=['GET'])
def getRecordList():
    res = {}
    path = os.path.join(os.path.expanduser('~'), 'records')
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    res["files"] = [k for k in onlyfiles if '.avi' in k]
    res["files"].sort(reverse=True)
    return jsonify(res), 200

def gen_video(name):
    path = os.path.join(os.path.expanduser('~'), 'records', name)
    video = CameraStream(path).startStream()
    while video:
        frame = video.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result
    video.stopStream()
@app.route('/showRecord')
def showRecord():
    name = request.args.get('name')
    if name:
        return Response(gen_video(name),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

#MAIN EXECUTE
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
