from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import psycopg2

# initialize our db
db = SQLAlchemy()
bcrypt = Bcrypt()

# connect to the db
conn = psycopg2.connect(
    host="localhost",
    database="pampermedb",
    user="postgres",
    password="pampermedb",
    port="5432"
)
