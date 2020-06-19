from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from book import books
from auth import auth
from order import order

app = Flask(__name__)
# for initial application config we should config from a file,
# because we need config our manager accounts initially...
# we still not have MySQL database, we need AWS account
# ================below is for testing======================
app.config['test'] = True
app.config['SECRET_KEY'] = 'Royal Never Give Up'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///....'

db = SQLAlchemy(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(books, url_prefix='/book')
app.register_blueprint(order, url_prefix='/order')

if __name__ == '__main__':
    app.run()
