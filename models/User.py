
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from passlib.hash import pbkdf2_sha256 as sha256
from App import session
from App import Base
import uuid


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    firstName = Column(String(80), unique=False, nullable=True)
    lastName = Column(String(80), unique=False, nullable=True)
    password = Column(String(80), nullable=False)
    age = Column(Integer, nullable=True)
    phoneNumber = Column(Integer, nullable=True)
    isBabysitter = Column(Boolean, nullable=False)

    def __init__(self, username, password, first_name, last_name, age, phone_number):
        self.id = uuid.uuid4()
        self.username = username
        self.password = password
        self.firstName = first_name
        self.lastName = last_name
        self.age = age
        self.phoneNumber = phone_number

    def save_to_db(self):
        session.add(self)
        session.commit()

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
