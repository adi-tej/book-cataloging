from app.main import db
from app.main.model.models import *
from app.main.model.user import User
from app.manage import app

# before running the application, it will make some pre-creating data
# for the database: there are three aspects: 1. opshops information 2.
# user information. 3. roles, this script will be executed at the terminal.

# ---> opshops information <---
with app.app_context():
    opshop_1 = Opshop()
    opshop_1.opshop_ebay_email = "weisong301@gmail.com"
    opshop_1.opshop_name = "opshop1"
    opshop_1.opshop_address = "Sydney, UNSW"
    opshop_1.staff_number = 4
    opshop_1.opshop_status = "running"

    db.session.add(opshop_1)
    db.session.commit()

    # ---> role information <---
    admin = Role(role_id=1, role_name='admin')
    user = Role(role_id=2, role_name='user')
    db.session.add_all([admin, user])
    db.session.commit()

    # ---> user information <---
    user1 = User(opshop_id=1, role_id=1, register_email='weisong301@gmail.com', user_name='Wei')
    user1.password('123456')
    user2 = User(opshop_id=1, role_id=2, register_email='kombasseril@gmail.com', user_name='Allen')
    user2.password('123456')
    user3 = User(opshop_id=1, role_id=2, register_email='admin@circex.com', user_name='Adi')
    user3.password('123456')
    user4 = User(opshop_id=1, role_id=2, register_email='nataliezhong08@gmail.com', user_name='Natalie')
    user4.password('123456')

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    # ---> item types <---
    itemtype1 = ItemType(item_type_id=1, item_type_name='book')

    db.session.add(itemtype1)
    db.session.commit()

