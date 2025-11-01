#step 3 now we need to create the routes for our application
from flask import Blueprint, render_template
from flask_login import login_required, current_user


#step 4 create blue print for views
views = Blueprint('views', __name__)

#step 6 start defining our views

@views.route('/')
@login_required
def home():
  return render_template("home.html", user= current_user) # noow we need to register these blueprints in init.py 


