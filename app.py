from flask import Flask, render_template, request
import re

app = Flask(__name__)

arr = ["hi","there","whats up maggots"]

def convertArrToString(array):
    s = ""
    for elements in array:
        s += elements+"<br/>"; #newline buat html pake <br/>
    return s

myString = convertArrToString(arr);

print(myString)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg') #INI YG BAKAL DIPROSES
    return myString


if __name__ == "__main__":
    app.run(debug = True)
