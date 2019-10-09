from marshmallow import fields, Schema
from root.models import bcrypt
import datetime
from root.models.Appointment import AppointmentSchema
from root.extensions import db


class Babysitter(db.Model):
    __tablename__ = 'babysitters'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    firstName = db.Column(db.String(80), unique=False, nullable=False)
    lastName = db.Column(db.String(80), unique=False, nullable=False)
    region = db.Column(db.String(80), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    phoneNumber = db.Column(db.Integer, nullable=True)
    experienceTime = db.Column(db.Integer, nullable=True)
    hourPrice = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    appointments = db.relationship('AppointmentModel', lazy=True)

    def __init__(self, data):
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))
        self.firstName = data.get('firstName')
        self.lastName = data.get('lastName')
        self.region = data.get('region')
        self.age = data.get('age')
        self.phoneNumber = data.get('phoneNumber')
        self.experienceTime = data.get('experienceTime')
        self.hourPrice = data.get('hourPrice')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # add this new method
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_babysitters():
        return Babysitter.query.all()

    def get_one_babysitter(id):
        return Babysitter.query.get(id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class BabysitterSchema(Schema):
    id = fields.Int(dump_only=True),
    username = fields.Email(required=True)
    password = fields.Str(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    region = fields.Str(required=False)
    age = fields.Str(required=True)
    phoneNumber = fields.Str(required=True)
    experienceTime = fields.Str(required=True)
    hourPrice = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    appointments = fields.Nested(AppointmentSchema, many=True)
