#encoding: utf-8

from exts import db
from datetime import datetime

# duty: boss, manager, staff, dimission
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    cellphone = db.Column(db.String(11), nullable=False)
    wechat = db.Column(db.String(100), nullable=False)
    duty = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    photopath = db.Column(db.String(255), nullable=True)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    cellphone = db.Column(db.String(11), nullable=False)
    wechat = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    left_myopia = db.Column(db.String(10), nullable=True)
    right_myopia = db.Column(db.String(10), nullable=True)
    left_astig = db.Column(db.String(10), nullable=True)
    right_astig = db.Column(db.String(10), nullable=True)
    score = db.Column(db.Integer, nullable = False)
    purchase = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(20), nullable = False)

class Glass(db.Model):
    __table__name = "glass"
    sku = db.Column(db.String(100), primary_key=True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    degree = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Eyedrop(db.Model):
    __tablename__ = 'eyedrop'
    sku = db.Column(db.String(100), primary_key=True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Nursing(db.Model):
    __tablename__ = 'nursing'
    sku = db.Column(db.String(100), primary_key=True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Washing(db.Model):
    __tablename__ = 'washing'
    sku = db.Column(db.String(100), primary_key=True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

class Consumption(db.Model):
    __tablename__ = 'consumption'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vip = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employeeId = db.Column(db.Integer, nullable=False)
    sku = db.Column(db.String(100), nullable=False)
    unitPrice = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.now())


class EmployeeLog(db.Model):
    __tablename__ = 'employeeLog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employeeId = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employeeName = db.Column(db.String(100), nullable=False)
    operation = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())




