from threading import Thread, Lock
import cv2
from flask import Flask, request, render_template, Response
from flask_cors import CORS
import json

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
def move():
   request.get_data()
   data = json.loads(request.data)
   try:
      recordVideo = str(data['recordVideo'])
   except KeyError:
      return "Missing data", 500

   if recordVideo:
      return "Start recording", 200
   else:
      return "Stop recording", 200

#MAIN EXECUTE
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
