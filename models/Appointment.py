import uuid
from db import db
from sqlalchemy import ForeignKey


class AppointmentModel(db.Model):
    __tablename__ = 'appointments'

    appointment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"))
    babysitter_id = db.Column(db.Integer, ForeignKey("babysitters.id"))
    start_date = db.Column(db.DateTime, unique=True, nullable=False)
    end_date = db.Column(db.DateTime, unique=True, nullable=False)

    def __init__(self, user_id, babysitter_id, start_date, end_date):
        self.appointment_id = uuid.uuid4()
        self.user_id = user_id
        self.babysitter_id = babysitter_id
        self.start_date = start_date
        self.end_date = end_date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(appointment_id=_id).first()
