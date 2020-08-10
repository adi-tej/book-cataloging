from app.main.model.models import *
from app.main.model.user import User
from setup_app import app

# before running the application, it will make some pre-creating data
# for the database: there are three aspects: 1. opshops information 2.
# user information. 3. roles, this script will be executed at the terminal.

# ---> opshops information <---
with app.app_context():
    opshop_1 = Opshop()
    opshop_1.opshop_ebay_email = "283301817@qq.com"
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
    user1 = User(opshop_id=1, role_id=1, email='weisong301@gmail.com', username='Wei')
    user1.password('123456')
    user2 = User(opshop_id=1, role_id=2, email='kombasseril@gmail.com', username='Allen')
    user2.password('123456')
    user3 = User(opshop_id=1, role_id=2, email='admin@circex.com', username='Adi')
    user3.password('123456')
    user4 = User(opshop_id=1, role_id=2, email='nataliezhong08@gmail.com', username='Natalie')
    user4.password('123456')

    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    # ---> item types <---
    itemtype1 = ItemType(item_type_id=1, item_type_name='book')

    db.session.add(itemtype1)
    db.session.commit()

