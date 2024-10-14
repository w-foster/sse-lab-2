from flask import Flask, render_template, request
import os

app = Flask(__name__, template_folder='../templates')


@app.route("/")
def hello_world():
	return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
	input_name = request.form.get("name")
	input_age = request.form.get("age")
	int_age = int(input_age)
	age_squared = int_age * int_age
	return render_template("hello.html", name=input_name, age=input_age, age_squared=age_squared)




