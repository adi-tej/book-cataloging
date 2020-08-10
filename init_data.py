from app.main.model.models import *
from app.main.model.user import User
from setup_app import app

# before running the application, it will make some pre-creating data
# for the database: there are three aspects: 1. opshops information 2.
# user information. 3. roles, this script will be executed at the terminal.

# ---> opshops information <---
with app.app_context():
    opshop = Opshop()
    opshop.email = "weisong301@gmail.com"
    opshop.name = "opshop1"
    opshop.address = "Sydney, UNSW"
    opshop.staff_count = 4
    opshop.status = "running"

    db.session.add(opshop)
    db.session.commit()

    # ---> role information <---
    admin = Role(id=1, name=RoleType.ADMIN)
    user = Role(id=2, name=RoleType.USER)
    db.session.add_all([admin, user])
    db.session.commit()

    # ---> user information <---
    user1 = User(opshop_id=1, role_id=1, email='admin@circex.com', name='Admin')
    user1.encrypt_password('123456')
    user2 = User(opshop_id=1, role_id=2, email='user@circex.com', name='Staff')
    user2.encrypt_password('123456')

    db.session.add_all([user1, user2])
    db.session.commit()

    # ---> item types <---
    itemtype1 = ItemType(id=1, name='book')

    db.session.add(itemtype1)
    db.session.commit()

