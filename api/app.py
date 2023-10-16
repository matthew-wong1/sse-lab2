from flask import Flask, render_template, request, make_response
app = Flask(__name__)
import sys

@app.route("/")
def index():
	# Return user data page if cookies are set 
	user_data = {}
	if len(request.cookies) != 0:
		for cookie in request.cookies:
			user_data[cookie] = request.cookies.get(cookie)

		return render_template("user_data.html", user_data=user_data)

	return render_template("index.html")

@app.route("/your_data", methods=["POST"])
def submit():
	# data from form 
	user_data = {} 

	user_data["name"] = request.form.get("name")
	user_data["age"] = request.form.get("age")
	user_data["tel"] = request.form.get("tel")
	user_data["email"] = request.form.get("email") 

	# data from request headers 
	user_agent = request.user_agent
	user_data["ip_address"] = request.remote_addr
	user_data["platform"] = user_agent.platform.capitalize()
	user_data["browser"] = user_agent.browser.capitalize()

	response = make_response(render_template("user_data.html", user_data=user_data))


	# set cookies for all inputted data 
	for key, value in user_data.items():
		response.set_cookie(key, value)

	return response

#Use cookies, dynamic forms. if c ookie value not empty, display form 
#Name, age (check that it is a number), UK number, make sure is ic.ac.uk email
#Your IP address is... 
#MAc address 
#(Maybe) what machine you are on 
#port number 

