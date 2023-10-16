from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
	# data from form 
	input_name = request.form.get("name")
	input_age = request.form.get("age")
	input_tel = request.form.get("tel")
	input_email = request.form.get("email") 

	# data from GET quest 
	ip_address = request.remote_addr
	return render_template("user_data.html", name=input_name, age=input_age, ip_address=ip_address)

#Use cookies, dynamic forms. if c ookie value not empty, display form 
#Name, age (check that it is a number), UK number, make sure is ic.ac.uk email
#Your IP address is... 
#MAc address 
#(Maybe) what machine you are on 
#port number 

