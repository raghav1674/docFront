#!/usr/bin/python3


from flask import Flask,request 
from docker import Docker

app = Flask(__name__)



@app.route("/containers",methods=['GET'])
def get_all():
    return Docker.get_all()

@app.route("/containers",methods=['POST'])
def create():
    
    name = request.form["name"]
    
    image = request.form["image"]
    
    new_container = Docker(name,image)

    return new_container.run() 
            


app.run(debug=True,host="192.168.56.103")

