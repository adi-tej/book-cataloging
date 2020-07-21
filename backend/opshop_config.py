from app import db
from model.models import Opshop

opshop_1 = Opshop()
opshop_1.opshop_ebay_email = "weisong301@gmail.com"
opshop_1.opshop_name = "Roland Book Store"
opshop_1.opshop_address = "Sydney, UNSW"
opshop_1.staff_number = 3
opshop_1.opshop_status = "running"

opshop_2 = Opshop()
opshop_2.opshop_ebay_email = "weisong301@gmail.com"
opshop_2.opshop_name = "Roland Book Store"
opshop_2opshop_address = "Sydney, UNSW"
opshop_2staff_number = 3
opshop_1.opshop_status = "running"

db.session.add(opshop_1)
db.session.commit()