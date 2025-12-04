# step 5 Now add the blueprints for auth also

from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import date 
from .models import User, Donor, Request, DonationInteraction
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import joinedload
from flask_login import current_user

auth = Blueprint('auth', __name__)

@auth.route("/")
@login_required 
def home():

    user_requests = Request.query.filter_by(requester_id=current_user.id).order_by(Request.id.desc()).all()
    is_donor = current_user.is_donor
    
    return render_template("home.html", user=current_user, user_requests=user_requests, is_donor=is_donor)

@auth.route("/remove_donor", methods=['POST'])
@login_required
def remove_donor():
    """Removes the current user's donor profile."""
    if current_user.is_donor:
        # Find and delete the donor entry
        donor_profile = Donor.query.filter_by(user_id=current_user.id).first()
        if donor_profile:
            db.session.delete(donor_profile)
            # Update the user flag
            current_user.is_donor = False
            db.session.commit()
            flash('You have been successfully removed from the donor list.', category='success')
        else:
            flash('Error: Donor profile not found.', category='error')
    else:
        flash('You are not currently registered as a donor.', category='error')
        
    return redirect(url_for('auth.home'))

@auth.route("/close_request/<int:request_id>", methods=['POST'])
@login_required
def close_request(request_id):
    """Changes the status of a specific request to 'Closed'."""
    # Ensure the request belongs to the current user
    req = Request.query.filter_by(id=request_id, requester_id=current_user.id).first()
    
    if req:
        # Only allow status change if it's currently 'Pending'
        if req.status == 'Pending':
            req.status = 'Closed'
            db.session.commit()
            flash(f'Request for {req.patient_name} successfully closed.', category='success')
        else:
            flash('This request is already closed.', category='error')
    else:
        flash('Request not found or you do not have permission to close it.', category='error')
        
    return redirect(url_for('auth.home'))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:    
            flash('First Name must be greater than 1 character.', category='error')
        elif password1 != password2:    
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:    
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit() 
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('auth.home'))
    return render_template("signup.html", user=current_user)


@auth.route("/register_donor", methods=['GET', 'POST'])
@login_required
def register_donor():
    if request.method == 'POST':
        blood_type = request.form.get('blood_type')
        age_str = request.form.get('age')
        contact_number = request.form.get('contact_number')
        city = request.form.get('city')

        try:
            age = int(age_str)
        except (ValueError, TypeError):
            flash('Invalid age provided.', category='error')
            return render_template("register_donor.html", user=current_user)

        if not current_user.is_donor:
            new_donor = Donor(user_id=current_user.id, blood_type=blood_type, age=age, contact_number=contact_number, city=city, last_donation_date=None)
            current_user.is_donor = True
            db.session.add(new_donor)
            db.session.commit()
            flash('You have been registered as a donor!', category='success')
        else:
            flash('You are already registered as a donor.', category='error')
    return render_template("register_donor.html", user = current_user)


@auth.route("/filter_donors")
@login_required
def filter_donors():
    all_donors = Donor.query.join(User).options(joinedload(Donor.user)).all()

    donor_list = []
    for donor in all_donors:
        donor_list.append({
            'blood_type': donor.blood_type,
            'age': donor.age,
            'contact_number': donor.contact_number
        })
    return render_template("filter_donors.html", user = current_user, donors=donor_list)


@auth.route("/view_requests")
@login_required
def view_requests():
    all_requests = Request.query.order_by(Request.id.desc()).all()
    return render_template("view_requests.html", user = current_user, requests=all_requests)


@auth.route("/make_request",methods=['GET', 'POST'])
@login_required
def make_request():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        blood_type_needed = request.form.get('blood_type_needed')
        units_needed_str = request.form.get('units_needed') 
        contact_number = request.form.get('contact_number')
        city = request.form.get('city')

        try:
            units_needed = int(units_needed_str)
        except (ValueError, TypeError):
            flash('Invalid units required provided. Please enter a number.', category='error')
            return render_template("make_request.html" ,user = current_user)
        
        if not patient_name or not blood_type_needed or not units_needed_str or not contact_number:
            flash('Please fill out all required fields for the request.', category='error')
            return render_template("make_request.html" ,user = current_user)

        new_request = Request(requester_id=current_user.id, patient_name=patient_name, blood_type_needed=blood_type_needed, units_needed=units_needed,contact_number=contact_number, city=city)
        db.session.add(new_request)
        db.session.commit()
        flash('Your blood request has been submitted!', category='success')
        return redirect(url_for('auth.view_requests'))
    return render_template("make_request.html" ,user = current_user)


@auth.route("/accept_donation", methods= ['POST'])
@login_required
def accept_donation():
    """
    Handles standard POST from the 'Accept' button:
    1. Records a new DonationInteraction.
    2. Updates the Donor's last_donation_date to today's date.
    3. Uses flash messages and redirects.
    """
    # *** CHANGE: Get data from request.form instead of request.get_json() ***
    request_id = request.form.get('request_id')

    if not request_id:
        flash("Missing request ID.", category='error')
        return redirect(url_for('auth.view_requests'))

    try:
        request_id = int(request_id)
    except (TypeError, ValueError):
        flash("Invalid request ID.", category='error')
        return redirect(url_for('auth.view_requests'))

    req = Request.query.get(request_id)
    if not req:
        flash("Request not found.", category='error')
        return redirect(url_for('auth.view_requests'))

    # Ensure the current user is registered as a donor and get their profile
    donor_profile = Donor.query.filter_by(user_id=current_user.id).first()
    if not donor_profile:
        flash("You must be registered as a donor to accept a request.", category='error')
        return redirect(url_for('auth.register_donor'))
    
    try:
        # 1. Record the new DonationInteraction
        new_interaction = DonationInteraction(
            donor_id=donor_profile.id, 
            request_id=req.id, 
            interaction_date=date.today(), # Use datetime.date.today()
            status='Accepted'
        )
        db.session.add(new_interaction)

        # 2. Update the Donor's last_donation_date (as requested)
        donor_profile.last_donation_date = date.today()
        # 2.5 Update the Request status to reflect acceptance
        req.status = 'Accepted'
        
        db.session.commit()

        
        
        # 3. Respond with flash and redirect
        flash(f"Donation accepted for {req.patient_name}. Your last donation date has been updated.", category='success')
        return redirect(url_for('auth.view_requests'))

    except Exception as e:
        db.session.rollback()
        print(f"Error accepting donation request: {e}")
        flash("An unexpected server error occurred while processing your request.", category='error')
        return redirect(url_for('auth.view_requests'))
    