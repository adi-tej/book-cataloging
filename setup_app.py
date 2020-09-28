from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from app.main import create_app, db
from app.app import blueprint

"""
    Create App with Environment
    ('production', 'development', 'test')
"""
app = create_app('development')
CORS(app)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run(host='0.0.0.0')


@manager.command
def drop_all():
    db.drop_all()


@manager.command
def create_all():
    db.create_all()


if __name__ == '__main__':
    manager.run()
