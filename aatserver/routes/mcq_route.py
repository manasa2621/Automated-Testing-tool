from flask import render_template, url_for, jsonify,request,redirect
from aatserver import app, db
from aatserver.modules.mcq_form import MCQuestions
from sqlalchemy import text



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/staff-login")
def login():
    return render_template("staff-login.html")

@app.route("/staffs-view")
def staffView():
    return render_template("staffview.html")

@app.route("/students-view")
def studentView():
    return render_template("studentview.html")

@app.route("/upload-mcq")
def multipleChoiceQuestions():
    form = MCQuestions()
    return render_template("multiplechoicequestion.html", title='MCQ View', form=form)
    


