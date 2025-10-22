# step 5 Now add the blueprints for auth also

from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return "<h1> Login </h1>"


@auth.route("/logout")
def logout():
    return "<h1> Logout </h1>"


@auth.route("register_donor")
def register_donor():
    return "<h1> Register Donor </h1>"


@auth.route("filter_donors")
def filter_donors():
    return "<h1> Filter Donors </h1>"


@auth.route("view_requests")
def view_requests():
    return "<h1> View Requests </h1>"


@auth.route("make_request")
def make_request():
    return "<h1> Make Request </h1>"
