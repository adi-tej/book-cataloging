import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.main import create_app, db

from app.main.model import user
from app.app import blueprint

app = create_app('dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    # db.drop_all()
    db.create_all()
    app.run()

if __name__ == '__main__':
    manager.run()
