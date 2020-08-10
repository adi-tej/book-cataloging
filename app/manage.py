import os
import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from app.main import create_app, db
from app import blueprint

app = create_app('dev')
CORS(app)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    # db.drop_all()
    # db.create_all()
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    manager.run()
