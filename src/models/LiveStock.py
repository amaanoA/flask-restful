#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from  db import db


class LiveStock(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    animal_type = db.Column(db.String(80))
    gender = db.Column(db.String(80),nullable=False)
    animal_id = db.Column(db.String(20), nullable=False, unique=True)
    age = db.Column(db.Float(2, 10), nullable=True)
    selling_price = db.Column(db.Float(2, 10), nullable=True)
    buying_price = db.Column(db.Float(2, 10), nullable=True)
    type_count = db.Column(db.Integer, nullable=False)

    # items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'public_id': self.public_id,'animal_type': self.animal_type,'animal_id': self.animal_id,
                'age': self.age,'selling_price': self.selling_price,'buying_price': self.buying_price,
                'type_count': self.type_count,
        }

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
