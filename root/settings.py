from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from root.app import app
from root.models import db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
