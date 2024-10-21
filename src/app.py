from flask import Flask, render_template, request, session
import random
import secrets

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
    else:
        return "Unknown"


if __name__ == "__main__":
    app.run(debug=True)
