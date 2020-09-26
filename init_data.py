from app.main.model.models import *
from app.main.model.user import User
from setup_app import app

# before running the application, it will make some pre-creating data
# for the database: there are three aspects: 1. opshops information 2.
# user information. 3. roles, this script will be executed at the terminal.

with app.app_context():

    '''
    DB INIT DATA
    '''

    # ---> opshops information <---
    opshop = Opshop()

    """
        Op-shop Ebay email
    """
    opshop.email = "circexunsw@gmail.com"
    opshop.name = "CircExUNSW1"
    opshop.address = "Perth"
    opshop.staff_count = 4

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

    '''
    TESTING DATA
    '''
    # ---> books <---
    book1 = Book(id=1, book_id_ebay=1, opshop_id=1, title='What If?', author='Randall Munroe',
                 cover='https://homepages.cae.wisc.edu/~ece533/images/boat.png', publisher='John Murray', edition=1,
                 price=7.99,status=ItemStatus.LISTED, ISBN_10='8273546373', description='')
    book2 = Book(id=2, book_id_ebay=2, opshop_id=1, title='Electronic Commerce', author='Gary P. Shneider',
                 cover='https://homepages.cae.wisc.edu/~ece533/images/monarch.png', publisher='Cengage Learning',
                 edition=1, price=139.95, status=ItemStatus.LISTED, ISBN_10='2355244373', description='')
    book3 = Book(id=3, book_id_ebay=3, opshop_id=1, title='The brief history of Time', author='Stephen Hawking',
                 cover='https://homepages.cae.wisc.edu/~ece533/images/watch.png', publisher='Bantam Books', edition=1,
                 price=8.99, status=ItemStatus.LISTED, ISBN_13='8273342373546', description='')
    db.session.add_all([book1, book2, book3])
    db.session.commit()
    # ---> images <---
    image1 = Image(id=1, item_id=1, uri='https://homepages.cae.wisc.edu/~ece533/images/boat.png')
    image2 = Image(id=2, item_id=2, uri='https://homepages.cae.wisc.edu/~ece533/images/monarch.png')
    image3 = Image(id=3, item_id=3, uri='https://homepages.cae.wisc.edu/~ece533/images/watch.png')
    image4 = Image(id=4, item_id=1, uri='https://homepages.cae.wisc.edu/~ece533/images/lena.png')
    db.session.add_all([image1,image2,image3,image4])
    db.session.commit()
    # ---> orders <---
    order1 = Order(id=1, opshop_id=1, status=OrderStatus.PENDING)
    order2 = Order(id=2, opshop_id=1, status=OrderStatus.PENDING)
    db.session.add_all([order1, order2])
    db.session.commit()

    db.session.add_all([OrderItem(order_id=1, item_id=1),OrderItem(order_id=1, item_id=3),OrderItem(order_id=2,item_id=2)])
    db.session.commit()
