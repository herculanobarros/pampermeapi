import uuid
import datetime
from marshmallow import fields, Schema
from root.extensions import db
from sqlalchemy import ForeignKey


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    babysitterId = db.Column(db.Integer, db.ForeignKey('babysitters.id'), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.user_id = data.get('userId')
        self.babysitter_id = data.get('babysitterId')
        self.description = data.get('description')
        self.created_at = data.get('startDate')
        self.modified_at = data.get('endDate')

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

    @staticmethod
    def get_all_appointment():
        return AppointmentModel.query.all()

    @staticmethod
    def get_one_appointment(id):
        return AppointmentModel.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class AppointmentSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    userId = fields.Int(required=True)
    babysitterId = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
