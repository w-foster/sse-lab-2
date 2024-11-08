from flask import Flask, render_template, request, session
import random
import secrets
import re
import requests
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Hardcoded session key for DEV ONLY


# Landing page; immediately starts new game
@app.route("/")
def landing():
    return new_game()


# Initialises session score variables to zero
@app.route("/new_game")
def new_game():
    session["total_answers_count"] = 0
    session["correct_answers_count"] = 0
    return question()


# Serves a randomly generated question
@app.route("/question")
def question():
    i = random.randint(0, 2)
    if i == 0:
        # addition
        random_one = random.randint(7, 62)
        random_two = random.randint(7, 62)
        random_operator = "+"
        session["correct_answer"] = random_one + random_two
    elif i == 1:
        # subtraction
        random_one = random.randint(5, 48)
        random_two = random.randint(5, 48)
        random_operator = "-"
        session["correct_answer"] = random_one - random_two
    elif i == 2:
        # multiplication
        random_one = random.randint(3, 12)
        random_two = random.randint(3, 12)
        random_operator = "*"
        session["correct_answer"] = random_one * random_two

    question_string = f"{random_one} {random_operator} {random_two}"
    return render_template("index.html", question=question_string)


# Checks user's answer and serves a results page
@app.route("/submit", methods=["POST"])
def submit():
    input_answer = int(request.form.get("answer"))
    session["total_answers_count"] += 1
    if input_answer == session["correct_answer"]:
        session["correct_answers_count"] += 1
        is_correct = True  # Used by front-end to display conditional messages
    else:
        is_correct = False
    if session["total_answers_count"] >= 5:
        return final_score()
    return render_template(
        "answer_result.html",
        correct_answer=session["correct_answer"],
        is_correct=is_correct,
        total_answers_count=session["total_answers_count"],
        correct_answers_count=session["correct_answers_count"],
    )


@app.route("/final_score")
def final_score():
    return render_template(
        "final_score.html",
        correct_answers_count=session["correct_answers_count"],
        total_answers_count=session["total_answers_count"],
    )


@app.route("/query", methods=["GET"])
def query():
    return process_query(request.args.get("q"))


def process_query(q):
    if q == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    if "largest" in q:
        nums = re.findall(r"\d+", q)
        numbers = [int(num) for num in nums]
        return str(max(numbers))
    if "power" in q:
        nums = re.findall(r"\d+", q)
        numbers = [int(num) for num in nums]
        return str(numbers[0] ** numbers[1])
    if "minus" in q:
        nums = re.findall(r"\d+", q)
        numbers = [int(num) for num in nums]
        return str(numbers[0] - numbers[1])
    if "What is" in q:
        nums = re.findall(r"\d+", q)
        numbers = [int(num) for num in nums]
        return str(numbers[0] + numbers[1] + numbers[2])
    else:
        return "Unknown"


# ==== GitHub Form (lab 5) ====


# Serves the user with a form to enter a GitHub username
@app.route("/github_form")
def github_form():
    return render_template("github_form.html")


# Endpoint redirected to after a submission to the github_form page
@app.route("/display_username", methods=["POST"])
def display_username():
    # Retrieve Tsuru env var: GitHub Access Token (for higher API rate limits)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    # Prepare a key/value pair with the token to use during requests
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    # Get the entered username and initialise a session var to store it
    username = request.form.get("github_username")
    session["github_username"] = username
    # Build an API URL, and make a call
    my_url = f"https://api.github.com/users/{username}/repos"
    rsp = requests.get(my_url, headers=headers)
    # Initialise a list containing every repo's info in JSON form
    repos = [r for r in rsp.json()] if rsp.status_code == 200 else []

    all_repos_info = []  # empty list to store the repo info dicts
    for repo in repos:
        this_repo_info = {}  # empty dict to store this repo's info
        # Store the repo's name and URL
        repo_name = repo.get("full_name", "Unknown")
        repo_url = repo.get("html_url", "N/A")

        # Store default values
        recent_hash = "No commits found!"
        recent_author = "N/A"
        recent_date = "N/A"
        recent_message = "N/A"
        recent_avatar = "https://t.ly/rH1hH"  # N/A img

        # Make another call to get info on commits
        commits_url = f"https://api.github.com/repos/{repo_name}/commits"
        commits_response = requests.get(commits_url, headers=headers)
        if commits_response.status_code == 200:
            commits = commits_response.json()
            if commits and isinstance(commits, list):
                recent_commit = commits[0]
                recent_author = recent_commit["commit"]["committer"]["name"]
                recent_date = recent_commit["commit"]["committer"]["date"]
                recent_message = recent_commit["commit"]["message"]
                recent_hash = recent_commit["sha"]
                if recent_commit["author"] is not None:
                    recent_avatar = recent_commit["author"]["avatar_url"]
                else:
                    recent_avatar = "https://picsum.photos/200"

        # Build out the dictionary for this repo
        this_repo_info["Avatar"] = recent_avatar
        this_repo_info["Repository Name"] = [repo_name, repo_url]
        this_repo_info["Author"] = recent_author
        this_repo_info["Date"] = recent_date
        this_repo_info["Hash"] = recent_hash
        this_repo_info["Message"] = recent_message
        # Add this repo's info to the list of dicts
        all_repos_info.append(this_repo_info)

    return render_template(
        "display_username.html",
        repos=all_repos_info,
        github_username=session["github_username"],
    )


if __name__ == "__main__":
    app.run(debug=True)
