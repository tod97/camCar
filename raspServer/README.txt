Before starting the project, exec those commands:

- pip install eventlet
- pip install flask-cors
- pip install socketio
- pip install python-socketio
- apt-get install python-opencv

After that, run:
- "api.py" to start the server for video stream (camera)
- "server.py" to start the server for socketio (controller)


IF U WANT:
- To run those scripts on startup:
  Run "sudo nano /etc/rc.local"
  Add 
    u pi -c 'python /home/pi/git/api.py &'
    u pi -c 'python /home/pi/git/server.py &'
