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


@app.route("/github_form")
def github_form():
    return render_template("github_form.html")


@app.route("/display_username", methods=["POST"])
def display_username():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    username = request.form.get("github_username")
    session["github_username"] = username
    my_url = f"https://api.github.com/users/{username}/repos"
    p = requests.get(my_url, headers=headers)
    # old = [r["full_name"] for r in p.json()] if p.status_code == 200 else []
    repos = [r for r in p.json()] if p.status_code == 200 else []
    if repos is None:
        return "User not found!"
    some_repos_info = []
    for repo in repos:
        some_repo_info = {}
        name = repo["full_name"]
        some_repo_info["Name"] = name
        # response = requests.get(repo[])
        url = f"https://api.github.com/repos/{name}/commits"
        commits_response = requests.get(url, headers=headers)
        if commits_response.status_code == 200:
            commits = commits_response.json()
            if commits:
                recent_commit = commits[0]
                recent_author = recent_commit["commit"]["committer"]["name"]
                recent_date = recent_commit["commit"]["committer"]["date"]
                recent_message = recent_commit["commit"]["message"]
                if recent_commit['author'] is not None:
                    recent_avatar = recent_commit["author"]["avatar_url"]
                else:
                    recent_avatar = "https://picsum.photos/200"
            else:
                recent_author = "No commits found!"
        else:
            recent_author = "Commit fetch failed"
        some_repo_info["Author"] = recent_author
        some_repo_info["Date"] = recent_date
        some_repo_info["Message"] = recent_message
        some_repo_info["Avatar"] = recent_avatar
        some_repos_info.append(some_repo_info)
    return render_template(
        "display_username.html",
        repos=some_repos_info,
        github_username=session["github_username"],
    )


if __name__ == "__main__":
    app.run(debug=True)
