from  db import db
from datetime import datetime



class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    # voucher_id = db.Column(db.Integer, db.ForeignKey("voucher.id"), nullable=True)
    # expense_voucher_id = db.Column(
    #     db.Integer, db.ForeignKey("expense_voucher.id"), nullable=True
    # )
    description = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    debit = db.Column(db.Float(10, 2), nullable=True)
    credit = db.Column(db.Float(10, 2), nullable=True)
    balance = db.Column(db.Float(10, 2), nullable=False)

    def json(self):
        return {'public_id': self.public_id,'name': self.name,'account_number': self.account_number,
                'balance': self.balance,"transactions": [transaction.json() for transaction in self.transactions.all()]
        }

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()
    
    
    @classmethod
    def sum_credit(cls,id):
        transactions = cls.query.filter_by(id=id).first()
        return {'credits': sum([tr.credit for tr in transactions])}
    
    @classmethod
    def sum_debits(cls,id):
        transactions = cls.query.filter_by(id=id).first()
        return {'debits': sum([tr.debit for tr in transactions])}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()