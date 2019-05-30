from main.db import db
from passlib.hash import pbkdf2_sha256 as sha256
import uuid


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstName = db.Column(db.String(80), unique=False, nullable=True)
    lastName = db.Column(db.String(80), unique=False, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    phoneNumber = db.Column(db.Integer, nullable=True)

    def __init__(self, username, password, first_name, last_name, age, phone_number):
        self.id = uuid.uuid4()
        self.username = username
        self.password = password
        self.firstName = first_name
        self.lastName = last_name
        self.age = age
        self.phoneNumber = phone_number

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def showAllUsers(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def deleteAllUsers(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} rows were delete'.format(num_rows_deleted)}
        except:
            return {'message': 'something went wrong.'}
