from flask import Flask, render_template, request
import random

app = Flask(__name__)


correct_answer = 0 # this will store the correct answer to the current Q

@app.route("/")
def hello_world():
    random_one = random.randint(3, 1000)
    random_two = random.randint(3, 1000)
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
    question = str(random_one + " " + random_operator + " " + random_two)
	return render_template("index.html", question=question)


@app.route("/submit", methods=["POST"])
def submit():
	input_answer = request.form.get("answer")
    int_input_answer = int(input_answer)

	age_squared = int_age * int_age
	return render_template("hello.html", name=input_name, age=input_age, age_squared=age_squared)


