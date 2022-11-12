#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from  db import db
from werkzeug.security import hmac
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    status = db.Column(db.String(20), nullable=True, default="Active")
    full_name = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    hired_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gender = db.Column(db.String(10), nullable=True)
    occupation = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Float(10, 2), nullable=False)

    def __init__(self, public_id, username, email, role, password,full_name,contact_number,
                 gender,occupation,salary,
                ):
        self.username = username
        self.password = password
        self.public_id = public_id
        self.email = email
        self.role = role
        self.full_name = full_name
        self.contact_number = contact_number
        self.gender = gender
        self.occupation = occupation
        self.salary = salary

    def json(self):
        return {'public_id':self.public_id, 'username': self.username, 'email': self.email,
                'role': self.role, 'status': self.status,'full_name': self.full_name,'contact_number': self.contact_number,
                'hired_date': self.hired_date.strftime('%m/%d/%Y'),'gender': self.gender,'occupation': self.occupation,'salary': str(round(self.salary,2))
                }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return hmac.compare_digest(self.password, password)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

