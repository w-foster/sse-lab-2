from flask import Flask, render_template, request
import random

app = Flask(__name__)


correct_answer = 0 # this will store the correct answer to the current Q

@app.route("/")
def hello_world():
    global correct_answer
    random_one = random.randint(3, 75)
    random_two = random.randint(3, 75)
    i = random.randint(0, 2)
    if i == 0:
        # addition
        random_operator = "+"
        correct_answer = random_one + random_two
    elif i == 1:
        # subtraction
        random_operator = "-"
        correct_answer = random_one - random_two
    elif i == 2:
        # multiplication
        random_operator = "*"
        correct_answer = random_one * random_two
    question_string = str(random_one) + " " + random_operator + " " + str(random_two)
    return render_template("index.html", question=question_string)


@app.route("/submit", methods=["POST"])
def submit():
    global correct_answer
    input_answer = int(request.form.get("answer"))
    if input_answer == correct_answer:
        is_correct = True
    else:
        is_correct = False
    return render_template("hello.html", correct_answer=correct_answer, is_correct=is_correct)


