#!/usr/bin/python
from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
masterId = ""


@app.route("/")
def main():
   return "Welcome to API", 200

@app.route('/connect',methods=['POST'])
def connect():
   global masterId
   request.get_data()
   data = json.loads(request.data)
   try:
      id = str(data['id'])
   except KeyError:
      return "Missing data", 500

   if masterId == "":
      print("User " + id + " is connected")
      masterId = id
      return "System connected", 200
   return "System busy", 500

@app.route('/move',methods=['POST'])
def move():
   global masterId
   request.get_data()
   data = json.loads(request.data)
   try:
      id = str(data['id'])
      position = str(data['position'])
   except KeyError:
      return "Missing data", 500

   if masterId == id:
      setMove()
      return "Moved to "+position, 200
   return "Can't move", 500


def setMove():
   print "TODO movimento motori"

if __name__ == "__main__":
   app.run(host= '0.0.0.0')