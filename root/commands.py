import click
from flask.cli import with_appcontext

from root.extensions import db
from root.models import Appointment, Babysitter, User, RevokedTokenModel


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()
