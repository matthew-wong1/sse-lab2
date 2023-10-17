from flask import Flask, render_template, request, make_response, redirect
from ua_parser import user_agent_parser 

app = Flask(__name__)

def check_name(name):
	return name.isalpha()

def check_age(age):
	return age.isnumeric() 

def check_tel(tel):
	if len(tel) == 10 and tel.isnumeric():
		return True

	return False

def check_email(email): 
	domain = email.split("@",1)[1]

	if domain == "ic.ac.uk":
		return True
	
	return False


@app.route("/")
def index():
	# Return user data page if cookies are set 
	user_data = {}
	if len(request.cookies) != 0:
		for cookie in request.cookies:
			user_data[cookie] = request.cookies.get(cookie)

		return render_template("user_data.html", user_data=user_data)

	return render_template("index.html")

@app.route("/your-data", methods=["POST"])
def submit():
	# data from form 
	user_data = {} 

	user_data["name"] = request.form.get("name")
	user_data["age"] = request.form.get("age")
	user_data["tel"] = request.form.get("tel")
	user_data["email"] = request.form.get("email") 

	name_is_valid = check_name(user_data['name'])
	age_is_valid = check_age(user_data['age'])
	tel_is_valid = check_tel(user_data['tel'])
	email_is_valid = check_email(user_data['email'])
	if (not(name_is_valid and age_is_valid and tel_is_valid and email_is_valid)):
		return redirect('/error')

	# data from request headers 
	user_agent_str = request.headers.get('User-Agent')
	user_data["ip_address"] = request.remote_addr
	user_data["platform"] = user_agent_parser.Parse(user_agent_str)['os']['family']
	user_data["browser"] = user_agent_parser.Parse(user_agent_str)['user_agent']['family']

	response = make_response(render_template("user_data.html", user_data=user_data))


	# set cookies for all inputted data 
	for key, value in user_data.items():
		response.set_cookie(key, value)

	return response

@app.route("/clear-cookies", methods=["POST"])
def clear_cookies():
	response = make_response(render_template("index.html"))
	for cookie in request.cookies:
		response.set_cookie(cookie, expires=0)
	return response; 

@app.route("/error", methods=["GET"])
def error():
	return render_template("error.html")
