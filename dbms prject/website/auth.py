# step 5 Now add the blueprints for auth also

from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/logout")
def logout():
    return render_template("login.html", boolean=True)

@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/register_donor")
def register_donor():
    return render_template("register_donor.html")


@auth.route("/filter_donors")
def filter_donors():
    return render_template("filter_donors.html")


@auth.route("/view_requests")
def view_requests():
    return render_template("view_requests.html")


@auth.route("/make_request")
def make_request():
    return render_template("make_request.html")
