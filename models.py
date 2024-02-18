from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    phonenum = db.Column(db.String(30), nullable=False)
    bottle_qty = db.Column(db.Integer)
    sachet_qty = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(255), default='New')

    def __repr__(self):
        return f'<request {self.id}>'
    
class Production_records(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bottle_qty = db.Column(db.Integer)
    sachet_qty = db.Column(db.Integer)    
    factory_worker = db.Column(db.String(255), nullable=False)
    production_date = db.Column(db.Date)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<production_records {self.id}>'
    
class User_profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    username = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    production_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    modified_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<production_records {self.id}>'

