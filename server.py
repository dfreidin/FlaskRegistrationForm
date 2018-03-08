from flask import Flask, render_template, request, redirect, session, flash
import re
import time
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z-]+$')
PW_REGEX = re.compile(r'[A-Z].*[0-9]|[0-9].*[A-Z]')
DATE_REGEX = re.compile(r'^(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])/[0-9]{4}$')
app = Flask(__name__)
app.secret_key = "swordfish"
@app.route('/')
def index():
    # print "index"
    return render_template('index.html')
@app.route("/check", methods=["POST"])
def check():
    em = request.form["email"]
    fn = request.form["first_name"]
    ln = request.form["last_name"]
    pw = request.form["password"]
    pw_c = request.form["confirm_pw"]
    bd = request.form["birth_date"]
    # print em+fn+ln+pw+pw_c
    valid = True
    if len(em) < 1:
        flash("No email address provided", "email")
        valid = False
    elif not EMAIL_REGEX.match(em):
        flash("Invalid email address", "email")
        valid = False
    if len(fn) < 1:
        flash("No first name provided", "first_name")
        valid = False
    elif not NAME_REGEX.match(fn):
        flash("First name should be letters only", "first_name")
        valid = False
    if len(ln) < 1:
        flash("No last name provided", "last_name")
        valid = False
    elif not NAME_REGEX.match(ln):
        flash("Last name should be letters only", "last_name")
        valid = False
    if len(pw) < 1:
        flash("No password provided", "password")
        valid = False
    elif len(pw) > 8:
        flash("Password is too long, no more than 8 characters", "password")
        valid = False
    elif not PW_REGEX.match(pw):
        flash("Password must contain at least 1 uppercase letter and 1 number", "password")
        valid = False
    if len(pw_c) < 1:
        flash("Must confirm password", "confirm_pw")
        valid = False
    elif pw_c != pw:
        flash("Password does not match", "confirm_pw")
        valid = False
    if len(bd) < 1:
        flash("No birth date provided", "birth_date")
        valid = False
    elif not DATE_REGEX.match(bd):
        flash("Birth date must be in MM/DD/YYYY format", "birth_date")
        valid = False
    elif time.strptime(bd, "%m/%d/%Y") >= time.localtime():
        flash("Birth date must be in the past", "birth_date")
        valid = False
    if valid:
        flash("Thanks for submitting your information", "good")
    # print valid
    return redirect("/")
app.run(debug=True)