from twodapp import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import date, datetime

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(admin_id)

class Bet(db.Model):
    __tablename__ = "bets"

    agent_rs = db.relationship('Agent')
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String,nullable=False)
    value = db.Column(db.String,nullable=False)
    time = db.Column(db.String)
    amount = db.Column(db.String,nullable=False)
    product = db.Column(db.Integer)
    amount_to_pay=db.Column(db.String,nullable=True,default="")
    state = db.Column(db.String,default="initial")
    agent_id = db.Column(db.Integer,db.ForeignKey('agents.id'))

    def __init__(self,date,value,amount,agent_id,time,product):
        self.date = date
        self.value = value
        self.amount = amount
        self.product = product
        self.time = time
        self.agent_id = agent_id

class Agent(db.Model):
    __tablename__ = "agents"
    id = db.Column(db.Integer,primary_key=True)
    start_date = db.Column(db.DateTime, nullable=True,default=datetime.utcnow)
    name = db.Column(db.String,nullable=False)
    bets = db.relationship('Bet',cascade="all,delete",backref="agent",lazy=True)
    balance=db.Column(db.String,default="0")
    total_amount=db.Column(db.String,default="0")

    def __init__(self,name):
        self.name = name

    def getNumberOfBets(self):
        return str(len(self.bets))
    
    def getTotalAmountOfBets(self):
        return int((self.total_amount))

    def getTotalAmountOfBetsString(self):
        return '{:0,.0f} Kyats'.format(int(self.total_amount))
    
    def getTotalBalance(self):
        return int(self.balance)

    def getTotalBalanceString(self):
        return '{:0,.0f} Kyats'.format(int(self.balance))
    
    def getSinceDuration(self):
        if self.start_date:
            return (str(self.start_date.day)+" - "+str(self.start_date.month)+" - "+str(self.start_date.year))
        else:
            return "Unknown"
            
class Admin(UserMixin,db.Model):

    __tablename__ = "admins"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,nullable=False,unique=True,index=True)
    password_hash = db.Column(db.String,nullable=False)

    def __init__(self,username,password_hash):
        self.username = username
        self.password_hash = generate_password_hash(password_hash)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def check_username(self,username):
        if self.username==username:
            return True
        else:
            return False

class TwoDigit(db.Model):
    __tablename__ = "twodigits"
    id = db.Column(db.Integer,primary_key=True)
    value = db.Column(db.Integer,nullable=False)
    time = db.Column(db.String)
    date = db.Column(db.String,nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,value,time,date):
        self.value = value
        self.date = date
        self.time = time

class ThreeDigit(db.Model):
    __tablename__ = "threedigits"
    id = db.Column(db.Integer,primary_key=True)
    value = db.Column(db.Integer,nullable=False)
    time = db.Column(db.String)
    date = db.Column(db.String,nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self,value,time,date):
        self.value = value
        self.date = date
        self.time = time