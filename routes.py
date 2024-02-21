from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Requests, Production_records, User_profiles
from sqlalchemy import desc, func
from datetime import datetime
import bcrypt
from users import User
# from app import login_manager
from login_loader import login_manager
from flask_bcrypt import check_password_hash


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def new():
    username = session.get('username')
    if request.method == 'POST':
        bottle_qty = request.form['bottle_qty']
        sachet_qty = request.form['sachet_qty']
        name = request.form['name']
        location = request.form['location']
        phonenum = request.form['phonenum']
        new_request = Requests(name=name, location=location, phonenum=phonenum, bottle_qty=bottle_qty, sachet_qty=sachet_qty)
        db.session.add(new_request)
        db.session.commit()
        new_request_id = new_request.id
        flash('Request submitted successfully!!!')
        return redirect(url_for('main.display_entry', id=new_request_id, username=username))
    return render_template('request/new.html', username=username)

@main_bp.route('/display/<int:id>', methods=['GET', 'POST'])
def display_entry(id):
    username = session.get('username')
    request_to_display = Requests.query.get_or_404(id)
    phonenum = request_to_display.phonenum
    related_requests = Requests.query.filter_by(phonenum=phonenum).all()
    return render_template('request/display.html', x=request_to_display, req=related_requests, username=username)

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_request(id):
    username = session.get('username')
    request_to_edit = Requests.query.get_or_404(id)
    if request.method == 'POST':
        # Process the form submission
        request_to_edit.bottle_qty = request.form['bottle_qty']
        request_to_edit.sachet_qty = request.form['sachet_qty']
        request_to_edit.name = request.form['name']
        request_to_edit.location = request.form['location']
        request_to_edit.phonenum = request.form['phonenum']
        request_to_edit.status = request.form['status']
        db.session.commit()
        flash('Request updated successfully!')
        return redirect(url_for('main.display_entry', id=id))
    # Render the form with the details of the specific request
    return render_template('request/edit.html', x=request_to_edit, username=username)

# Routes for Production user story
@main_bp.route('/admin', methods=('GET', 'POST'))
def admin():
    username = session.get("username")
    fullname = session.get("full_name")
    if username == None:
        flash("Please Login to Access this page!", "error")
        return redirect(url_for("main.login"))
    else:
        active_requests = Requests.query.filter(Requests.status.notin_(['canceled', 'completed'])).order_by(desc(Requests.modified_date)).all()
        return render_template('admin/home.html', x=active_requests, fullname=fullname, username=username)

@main_bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    username = session.get("username")
    if username == None:
        flash("Please Login to access this page", "error")
        return redirect(url_for("main.login"))
    else:
        entries = Requests.query.filter(Requests.status.notin_(['Canceled', 'Delivered'])).order_by(desc(Requests.modified_date)).all()

        # Fetching count of entries based on status
        new_count = db.session.query(func.count(Requests.id)).filter(Requests.status == 'New').scalar()
        enroute_count = db.session.query(func.count(Requests.id)).filter(Requests.status == 'On route').scalar()
        delivered_count = db.session.query(func.count(Requests.id)).filter(Requests.status == 'Delivered').scalar()
        canceled_count = db.session.query(func.count(Requests.id)).filter(Requests.status == 'Canceled').scalar()
    
        # Fetching Production data
        bottle_sum = db.session.query(func.sum(Production_records.bottle_qty)).scalar()
        sachet_sum = db.session.query(func.sum(Production_records.sachet_qty)).scalar()

        return render_template('admin/dashboard.html', x=entries, new=new_count, username=username, enroute=enroute_count, delivered=delivered_count, canceled=canceled_count, bottled=bottle_sum, sachet=sachet_sum)

@main_bp.route('/add_production', methods=['GET', 'POST'])
def add_production():
    username = session.get("username")
    fullname = session.get("full_name")
    if username == None:
        flash("Please Login to access this page!", "error")
        return redirect(url_for("main.login"))
    else:
        if request.method == 'POST':
            bottle_qty = request.form['bottle_qty']
            sachet_qty = request.form['sachet_qty']
            factory_worker = request.form['factory_worker']
            production_date_str = request.form['production_date']
            production_date = datetime.strptime(production_date_str, '%Y-%m-%d')

            # Insert the new production data into the production_records table
            new_prod = Production_records(bottle_qty=bottle_qty, sachet_qty=sachet_qty, factory_worker=factory_worker, production_date=production_date)
            db.session.add(new_prod)
            db.session.commit()
            new_prod_id = new_prod.id
            flash('Production form submitted successfully!!!')
            return redirect(url_for('main.display_production', id=new_prod_id))
        return render_template('admin/add_production.html', fullname=fullname)

@main_bp.route('/display_production/<int:id>', methods=['GET', 'POST'])
def display_production(id):
    username = session.get('username')
    if username == None:
        flash("Please Login to access this page", "error")
        return redirect(url_for("main.login"))
    else:
        prod_to_display = Production_records.query.get_or_404(id)
        return render_template('admin/display_production.html', x=prod_to_display)

@main_bp.route('/production_content', methods=['GET', 'POST'])
def production_content():
    username = session.get("username")
    if username == None:
        flash("Please login to access this page", "warning")
        return redirect (url_for("main.login"))
    else:
        prod_records = Production_records.query.order_by(desc(Production_records.modified_date)).all()
        return render_template('admin/production_content.html', x=prod_records, username=username)

@main_bp.route('/edit_production/<int:id>', methods=['GET', 'POST'])
def edit_production(id):
    username = session.get('username')
    prod_to_edit = Production_records.query.get_or_404(id)
    if request.method == 'POST':
        # Process the form submission
        prod_to_edit.bottle_qty = request.form['bottle_qty']
        prod_to_edit.sachet_qty = request.form['sachet_qty']
        prod_to_edit.factory_worker = request.form['factory_worker']
        production_date_str = request.form['production_date']
        prod_to_edit.production_date = datetime.strptime(production_date_str, '%Y-%m-%d')
        db.session.commit()
        flash('Production updated successfully!')
        return redirect(url_for('main.production_content'))
    # Render the form with the details of the specific request
    return render_template('admin/edit_production.html', x=prod_to_edit, username=username)

#Route to handle search
@main_bp.route('/search')
def search():
    username = session.get('username')
    query = request.args.get('query', '').strip().lower()
    results = []
                                                  
    if not query:
        message = "Enter a search criteria in the input box"
    else:
        results = Requests.query.filter(
            db.or_(
                Requests.name.ilike(f"%{query}%"),
                Requests.phonenum.ilike(f"%{query}%")
            )
        ).all()
        if not results:
            message = f"No results found for '{query}'."
        else:
            message = f"Search results for '{query}':"

    return render_template('common/search.html', results=results, message=message, username=username)


@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        fullname = request.form['full_name']
        password = request.form['password']
        second_password = request.form['enter_password_again']
        
        if password != second_password:
            flash('Passwords differ. Make sure passwords match!', "error")
            return redirect(url_for("main.register"))
        else:
            # Hash the password before storing it in the database
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())    
            # Check if the username or email already exists
            existing_user = User_profiles.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists! Please choose a different username.", "error")
                return redirect(url_for("main.register"))
                
            existing_email = User_profiles.query.filter_by(email=email).first()
            if existing_email:
                flash("Email already exists! Please use a different email.", "error")
                return redirect(url_for("main.register"))
        
            # Create a new user
            new_user = User_profiles(username=username, email=email, full_name=fullname, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
        
            flash("Registration successful! You can now login.")
            return redirect(url_for("main.login"))
    return render_template('user_profile/register.html')



@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User_profiles.query.filter_by(username=username).first()
        print(user)
        # Check if the user exists and if the provided password matches the hashed password
        if user and check_password_hash(user.password, password):
            session['username'] = username
            # session['full_name'] = fullname
            # session['email'] = email
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "error")
    return render_template('user_profile/login.html')


@main_bp.route('/profile')
def profile():
    username = session.get('username')
    fullname = session.get('full_name')
    email = session.get('email')
    
    if username:
        user = User_profiles.query.filter_by(username=username).first()
        if user:
            return render_template('user_profile/profile.html', user=user, username=username, fullname=fullname, email=email)
    flash('User profile not found!', 'error')
    return redirect(url_for('main.new'))



@main_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.new'))


@main_bp.errorhandler(404)
def not_found_error():
    return render_template('error/404.html'), 404

@main_bp.errorhandler(503)
def service_unavailable_error(error):
    return render_template('error/503.html', error=error), 503

@main_bp.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html', error=error), 500