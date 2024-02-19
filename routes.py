from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Requests, Production_records
from sqlalchemy import desc, func, case, literal_column
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('request/new.html')

@main_bp.route('/', methods=['GET', 'POST'])
def new():
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
        return redirect(url_for('main.display_entry', id=new_request_id))
    return render_template('request/new.html')

@main_bp.route('/display/<int:id>', methods=['GET', 'POST'])
def display_entry(id,):
    request_to_display = Requests.query.get_or_404(id)
    phonenum = request_to_display.phonenum
    related_requests = Requests.query.filter_by(phonenum=phonenum).all()
    return render_template('request/display.html', x=request_to_display, req=related_requests)

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_request(id):
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
    return render_template('request/edit.html', x=request_to_edit)

# Routes for Production user story
@main_bp.route('/admin', methods=('GET', 'POST'))
def admin():
    active_requests = Requests.query.filter(Requests.status.notin_(['canceled', 'completed'])).order_by(desc(Requests.modified_date)).all()
    return render_template('admin/home.html', x=active_requests)

@main_bp.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    entries = db.session.query(Requests.id, Requests.name, Requests.location, Requests.phonenum, Requests.status) \
    .filter(Requests.status.notin_(['canceled', 'delivered'])) \
    .order_by(Requests.modified_date.desc()) \
    .all()

    # Fetching count of entries based on status
    
    
    #Fetching Production data
    bottle_sum = db.session.query(func.sum(Production_records.bottle_qty)).scalar()
    sachet_sum = db.session.query(func.sum(Production_records.sachet_qty)).scalar()

    return render_template('admin/dashboard.html', x=entries, bottled=bottle_sum, sachet=sachet_sum)

@main_bp.route('/add_production', methods=['GET', 'POST'])
def add_production():
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
        flash('Production form submitted successfully!!!')
        # username = session.get("username")
        return redirect(url_for('main.production_content'))
    return render_template('admin/add_production.html')

@main_bp.route('/production_content', methods=['GET', 'POST'])
def production_content():
    prod_records = Production_records.query.order_by(desc(Production_records.modified_date)).all()
    return render_template('admin/production_content.html', x=prod_records)

@main_bp.route('/edit_production/<int:id>', methods=['GET', 'POST'])
def edit_production(id):
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
    return render_template('admin/edit_production.html', x=prod_to_edit)

# Routes to handle 404 and 503 errors
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@main_bp.errorhandler(503)
def service_unavailable_error(error):
    return render_template('error/503.html', error=error), 503
