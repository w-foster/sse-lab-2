from flask import Flask, render_template, request, session
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32) # Hardcoded session key for DEVELOPMENT ONLY


@app.route("/")
def landing():
    return new_game()

@app.route("/new_game")
def new_game():
    session["total_answers_count"] = 0
    session["correct_answers_count"] = 0
    return question()

@app.route("/question")
def question():
    i = random.randint(0, 2)
    if i == 0:
        # addition
        random_one = random.randint(3, 75)
        random_two = random.randint(3, 75)
        random_operator = "+"
        session["correct_answer"] = random_one + random_two
    elif i == 1:
        # subtraction
        random_one = random.randint(3, 54)
        random_two = random.randint(3, 54)
        random_operator = "-"
        session["correct_answer"] = random_one - random_two
    elif i == 2:
        # multiplication
        random_one = random.randint(3, 12)
        random_two = random.randint(3, 12)
        random_operator = "*"
        session["correct_answer"] = random_one * random_two
    question_string = str(random_one) + " " + random_operator + " " + str(random_two)
    question_string = f"{random_one} {random_operator} {random_two}"
    return render_template("index.html", question=question_string)

@app.route("/submit", methods=["POST"])
def submit():
    input_answer = int(request.form.get("answer"))
    session["total_answers_count"] += 1
    if input_answer == session["correct_answer"]:
        session["correct_answers_count"] += 1
        is_correct = True  # Used by front-end to show whether ans was correct or not
    else:
        is_correct = False
    return render_template("answer_result.html", correct_answer=session["correct_answer"], is_correct=is_correct, total_answers_count=session["total_answers_count"], correct_answers_count=session["correct_answers_count"])



