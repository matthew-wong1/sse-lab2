import re
import requests
from pydantic import BaseModel
from datetime import datetime
from flask import Flask, make_response, redirect, render_template, request
from ua_parser import user_agent_parser

app = Flask(__name__)


def process_query(input_string):
    if input_string == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif "name" in input_string:
        return "itsarainyday"
    elif "largest" in input_string:
        num_list = re.findall(r'\d+', input_string)
        result = list(map(int, num_list))
        return str(max(result))
    elif "plus" in input_string:
        num_list = re.findall(r'\d+', input_string)
        result = list(map(int, num_list))
        return str(sum(result))
    elif "mult" in input_string:
        num_list = re.findall(r'\d+', input_string)
        results = list(map(int, num_list))
        return str(results[0] * results[1])
    elif "square" in input_string:
        num_list = re.findall(r'\d+', input_string)
        results = list(map(int, num_list))
        answers = []
        for result in results:
            cube_root = result**(1./3.)
            sqrt = result**(1/2)
            rounded_cube = round(cube_root)**3
            rounded_sqrt = round(sqrt)**2
            if result == rounded_cube and result == rounded_sqrt:
                answers.append(result)
        if len(answers) == 1:
            return str(answers[0])
        else:
            final_answer = str(answers).replace('[', '')
            final_answer = final_answer.replace(']', '')
            return final_answer
    elif "minus" in input_string:
        num_list = re.findall(r'\d+', input_string)
        results = list(map(int, num_list))
        return str(results[0] - results[1])
    elif "primes" in input_string:
        num_list = re.findall(r'\d+', input_string)
        results = list(map(int, num_list))
        answers = []
        for result in results:
            if result == 1:
                continue
            for i in range(2, int(result/2)+1):
                if result % i == 0:
                    break
            else:
                answers.append(result)

        return str(answers)
    else:
        return "Unknown"


def check_name(name):
    return name.isalpha()


def check_age(age):
    return age.isnumeric()


def check_tel(tel):
    if len(tel) == 10 and tel.isnumeric():
        return True

    return False


def check_email(email):
    domain = email.split("@", 1)[1]

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

    name_is_valid = check_name(user_data["name"])
    age_is_valid = check_age(user_data["age"])
    tel_is_valid = check_tel(user_data["tel"])
    email_is_valid = check_email(user_data["email"])
    if not (name_is_valid and
            age_is_valid and
            tel_is_valid and
            email_is_valid):
        return redirect("/error")

    # data from request headers
    user_agent_str = request.headers.get("User-Agent")
    user_data["ip_address"] = request.remote_addr
    user_data["platform"] = \
        user_agent_parser.Parse(user_agent_str)["os"]["family"]
    user_data["browser"] = \
        user_agent_parser.Parse(user_agent_str)["user_agent"]["family"]

    response = \
        make_response(render_template("user_data.html", user_data=user_data))

    # set cookies for all inputted data
    for key, value in user_data.items():
        response.set_cookie(key, value)

    return response


@app.route("/clear-cookies", methods=["POST"])
def clear_cookies():
    response = make_response(render_template("index.html"))
    for cookie in request.cookies:
        response.set_cookie(cookie, expires=0)
    return response


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")


@app.route("/query", methods=["GET"])
def query():
    q = request.args.get('q')
    return process_query(q)


@app.route("/github", methods=["GET", "POST"])
def github():
    if request.method == "POST":
        try:
            if 'findUser' in request.form:
                username = request.form.get("username")
                url = "https://api.github.com/users/{username}/repos".format(username = username)
                query_parameters = {
                    "sort":"updated",
                    "direction":"desc"
                }
                response = requests.get(url, params=query_parameters)
                data = response.json()  # data returned is a list of ‘repository’ entities
                info_list = []
                repo_urls = []
                repos_list = []
                for i in data:
                    temp_dict = dict((key, i[key]) for key in ('name', 'created_at','html_url','updated_at','visibility','forks','watchers'))
                    temp_dict["repo_name"] = temp_dict.pop("name")
                    info_list.append(temp_dict)
                    repo_urls.append("https://api.github.com/repos/{username}/".format(username=username)+i["name"] + "/commits")
                for repo_url in repo_urls:
                    data_temp = requests.get(repo_url).json()
                    try: 
                        commit = data_temp[0]
                        commit_details = commit["commit"]["committer"]
                        temp_dict = dict((key, commit_details[key]) for key in ('name','date'))
                        temp_dict["sha"] = commit["sha"]
                        temp_dict['message'] = commit["commit"]["message"]
                        repos_list.append(temp_dict)
                    except: 
                        repos_list.append({"name": "",
                                            "date": "1990-01-01T00:00:00Z",
                                            "message": "",
                                            "sha": ""})
                        continue 
                
                    combined_list = []
                    for dict1, dict2 in zip(info_list,repos_list):
                        combined_list.append({**dict1, **dict2})
                    
                    class Repo(BaseModel):
                        created_at: datetime
                        html_url: str
                        updated_at: datetime
                        visibility: str 
                        forks: int 
                        watchers: int 
                        repo_name: str 
                        name: str
                        date: datetime 
                        message: str 
                        sha: str 

                    class_list = []
                    for i in combined_list:
                        repo = Repo(**i)
                        class_list.append(repo)

                return render_template("githubresponse.html", username = username, repos=class_list)
  
            elif 'findIssue' in request.form:
                keyword = request.form.get("keyword")
                if (keyword):
                    keyword += "+"
                language = request.form.get("language")
                date = request.form.get("date")
                url = "https://api.github.com/search/issues?q={keyword}language:{language}+date:>={date}+archived:false+state:open+no:assignee+is:public+label:bug".format(keyword=keyword, date=date, language=language)
                print(url)
                response = requests.get(url)
                if response.status_code == 200:
                    issues = response.json()
                return render_template("randomissue.html", issues=issues)
        except:
            return render_template("errorgithub.html")
    else:
        return render_template("github.html")
