from  db import db
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    balance = db.Column(db.Float(2, 10), nullable=False)

    transactions = db.relationship("Transaction", backref="account", lazy="dynamic")

    def __init__(self,public_id,name,account_number,balance):
        self.public_id = public_id
        self.name = name
        self.account_number = account_number
        self.balance = balance
        


    def json(self):
        return {'public_id': self.public_id,'name': self.name,'account_number': self.account_number,
                'balance': self.balance,"transactions": [transaction.json() for transaction in self.transactions.all()]
        }

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
    @classmethod
    def increase_balance(cls, amount,id):
        acount = cls.query.filter_by(id=id).first()
        acount.balance += amount
        db.session.commit()
        return {'balance':acount.balance}
    
    @classmethod
    def decrease_balance(cls, amount,id):
        acount = cls.query.filter_by(id=id).first()
        acount.balance -= amount
        db.session.commit()
        return {'balance':acount.balance}
    
    def get_acount_balance(self):
        return {'balance': self.balance}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()