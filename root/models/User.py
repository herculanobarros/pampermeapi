
from marshmallow import fields, Schema
from root.models import bcrypt
from root.models.Appointment import AppointmentSchema
import datetime
from root.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    firstName = db.Column(db.String(100), unique=False, nullable=False)
    lastName = db.Column(db.String(100), unique=False, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(5000), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    phoneNumber = db.Column(db.Integer, nullable=True)
    appointments = db.relationship('AppointmentModel', backref='appointments', lazy=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    # add this new method
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
            self.modified_at = datetime.datetime.utcnow()
            db.session.commit()

    def __init__(self, data):
        self.username = data.get('username')
        self.firstName = data.get('firstName')
        self.lastName = data.get('lastName')
        self.description = data.get('description')
        self.age = data.get('age')
        self.phoneNumber = data.get('phoneNumber')
        self.password = self.__generate_hash(data.get('password'))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Email(required=True)
    password = fields.Str(required=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    description = fields.Str(required=False)
    age = fields.Str(required=True)
    phoneNumber = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    appointments = fields.Nested(AppointmentSchema, many=True)