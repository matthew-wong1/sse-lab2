from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
	input_name = request.form.get("name")
	input_age = request.form.get("age")
	input
	return render_template("hello.html", name=input_name, age=input_age)

#Use cookies, dynamic forms. if c ookie value not empty, display form 
#Name, age (check that it is a number), UK number, make sure is ic.ac.uk email
#Your IP address is... 
#MAc address 
#(Maybe) what machine you are on 
#port number 

