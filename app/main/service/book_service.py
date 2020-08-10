from flask import jsonify, make_response
from datetime import datetime
from ebaysdk.trading import Connection
import json
import requests
from uuid import uuid1
import shutil
import boto3
from botocore.client import Config
from app.main.model.models import Image, Book, ItemStatus, ItemCondition
from app.main.model.user import User
from ..util.decorator import TOKEN
from .. import db
from app.main.config import EbayConfig


def find_book_info(isbn):  # function to search book in both api
    book_info = extract_data_google_api(isbn)
    if book_info == 0:
        # print("didnt get in google books")
        book_info = extract_isbndb_api(isbn)
    if book_info == 0:
        # print("didnt get in isbndb")
        return {}  # book info not found in both api,return empty dictionary

    return book_info


def extract_data_google_api(isbn):
    API_KEY = "AIzaSyD6-khCY5wCvJbq0JYCIyw75gfxTtgHt_o"  # google api key
    google_url_book = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}&key={}".format(isbn,
                                                                                            API_KEY)  # 9781925483598
    response = requests.get(google_url_book)
    data = response.text

    parsed = json.loads(data)

    book_data = {}  # empty dictionary

    if parsed['totalItems'] == 0:
        print("item not found in google api ")
        return 0  # return 0 when item not found

    book_info = parsed['items'][0]
    try:
        book_data['title'] = book_info['volumeInfo']['title']
    except:
        book_data['title'] = "NA"
    try:
        book_data['author'] = book_info['volumeInfo']['authors'][0]
    except:
        book_data['author'] = "NA"
    try:
        book_data['genre'] = book_info['volumeInfo']['categories'][0]
    except:
        book_data['genre'] = "NA"
    try:
        book_data["publisher"] = book_info['volumeInfo']['publisher']
    except:
        book_data["publisher"] = "NA"
    try:
        book_data["publish_date"] = book_info['volumeInfo']['publishedDate']
    except:
        book_data["publish_date"] = "NA"
    try:
        book_data["page_count"] = book_info['volumeInfo']['pageCount']
    except:
        book_data["page_count"] = "NA"
    try:
        book_data["description"] = book_info['volumeInfo']['description']
    except:
        book_data["description"] = "NA"
    try:
        book_data['cover'] = book_info['volumeInfo']['imageLinks']['thumbnail']
    except:
        pass
    try:
        book_data["ISBN_10"] = book_info['volumeInfo']['industryIdentifiers'][1]['identifier']
    except:
        book_data['ISBN_10'] = "NA"

    try:
        book_data["ISBN_13"] = book_info['volumeInfo']["industryIdentifiers"][0]['identifier']
    except:
        book_data["ISBN_13"] = "NA"

    return book_data  # return book object


def extract_isbndb_api(ISBN):
    isbn_url_book = "https://api2.isbndb.com/book/{}".format(ISBN)
    h = {'Authorization': '44245_0eebc755e9df899dbcdd5121c6cca21f'}
    response = requests.get(isbn_url_book, headers=h)
    data = response.text
    parsed = json.loads(data)
    print("parsed in function ISBNDB ", parsed)
    book_info = parsed.get("book")

    book_data = {}  # empty dictionary
    if book_info:

        try:
            book_data['title'] = book_info['title']
        except:
            book_data["title"] = "NA"
        try:
            book_data['author'] = book_info['authors'][0]
        except:
            book_data["author"] = "NA"
        try:
            book_data["publisher"] = book_info['publisher']
        except:
            book_data['publisher'] = "NA"

        try:
            book_data["page_count"] = book_info['pages']
        except:
            book_data["page_count"] = "NA"
        try:
            book_data['cover'] = book_info['image']
        except:
            pass

        try:
            book_data["ISBN_10"] = book_info["isbn"]
        except:
            book_data["ISBN_10"] = 'NA'
        try:
            book_data["ISBN_13"] = book_info["isbn13"]
        except:
            book_data['ISBN_13'] = "NA"

        return book_data

    else:

        return 0  # return 0 when item not found


def upload_to_s3(body, name):
    ACCESS_KEY_ID = 'AKIA5WMHZHLO4GDCKDO6'
    ACCESS_SECRET_KEY = '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'
    BUCKET_NAME = 'circexunsw'

    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    # image upload
    s3.Bucket(BUCKET_NAME).put_object(Key=name, Body=body)

    return


def retrive_book(data):
    # print(data["ISBN"],type(data['ISBN']))

    book_data = find_book_info(data)
    if book_data:
        book_data['id'] = uuid1()
        book_data['book_id_ebay'] = ''
        book_data['item_type_id'] = 1
        book_data['created_date'] = datetime.now()
        book_data['updated_date'] = datetime.now()
        book_data['status'] = 'unlisted'

        try:  ##here we can get a key error while accesing book_data['cover'] if no info was recoverd from api's.

            image_r = requests.get(book_data['cover'], stream=True)

            if image_r.status_code == 200:  # if image retrieved succesfully
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                image_r.raw.decode_content = True
                # print(image_r.raw.read())

                file_name = 'example.png'

                # Open a local file with wb ( write binary ) permission.
                with open(file_name, 'wb') as new_file:
                    shutil.copyfileobj(image_r.raw, new_file)

                bookcover = open(file_name, 'rb')  # opening the saved image
                key = str(book_data['id']) + '/cover.png'
                upload_to_s3(bookcover, key)  # image saved to amazon s3
                bookcover.close()
                file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)
                book_data['cover'] = file_url  ## amazon url of file overwritten in Book['cover']
                new_file.close()
                # os.remove(file_name)
                # print("Attachment Successfully save in S3 Bucket url %s " % (file_url))

        except KeyError:
            book_data['cover'] = None

    book = Book()

    book.__dict__ = book_data

    return book


def update_book(data, images, book_id):
    book = Book.query.filter_by(id=book_id).first()  # fetching saved book info from table

    if book:

        book_data = book.__dict__

        for key, value in data.items():
            setattr(book, key, value)

        image_number = 0
        for x in images:
            image_number = image_number + 1
            image = images[x]
            image.save(str(image_number) + '.png')
            body = open(str(image_number) + '.png', 'rb')
            key = str(book_id) + '/' + str(image_number) + '.png'

            upload_to_s3(body, key)
            body.close()
            file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)

            image_dict = {}  # dictionary analogues to Image object
            if image_number == 1:  # updating  the new  1st image as cover
                book.cover = file_url

            image_object = Image()
            image_dict['item_id'] = book_data['id']
            image_dict['aws_link'] = file_url
            temp = image_object.__dict__
            image_dict['_sa_instance_state'] = temp['_sa_instance_state']
            image_object.__dict__ = image_dict

            db.session.add(image_object)
            db.session.commit()

        db.session.commit()

    return book


def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return book


def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        resp = make_response(jsonify(book.__dict__))
        db.session.remove(book)
        db.session.commit()

    return book


def list_book(book):
    if book:
        # build connection with ebay
        # make request body to ebay
        # execute request to ebay and get response
        try:
            ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
            request_info = {
                "Item": {
                    "Title": book.title + " " + book.id,
                    "PictureDetails": {
                        # This URL shold be replaced by Allen after finishing S3 storage
                        "PictureURL": book.cover,
                    },

                    "PrimaryCategory": {
                        "CategoryID": "2228",
                    },

                    "Country": "AU",
                    "Location": book.opshop.address,
                    "Site": "Australia",
                    "SiteID": 15,
                    "ConditionID": book.condition,
                    "PaymentMethods": "PayPal",
                    "PayPalEmailAddress": book.opshop.email,
                    "Description": book.description,
                    "ListingDuration": "Days_30",
                    "StartPrice": book.price,
                    "ListingType": "FixedPriceItem",
                    "Currency": "AUD",
                    "ReturnPolicy": {
                        "ReturnsAcceptedOption": "ReturnsAccepted",
                        "RefundOption": "MoneyBack",
                        "ReturnsWithinOption": "Days_30",
                        "ShippingCostPaidByOption": "Buyer"
                    },
                    "ShippingDetails": {
                        "ShippingServiceOptions": {
                            "FreeShipping": "True",
                            "ShippingService": "AU_Express"
                        }
                    },
                    "DispatchTimeMax": "3"
                },
            }
            ebay_conn.execute("AddItem", request_info)
            # update ebay id

        except Exception:
            print("error")
            deletedbook = delete_book(book.id)
            # "should give 500"
            return deletedbook

        book.status = 'listed'
        db.session.commit()

        # print("BOok returned from confirm",bookobject.__dict__)

    return book


def list2_book(book_id):
    book = Book.query.filter_by(book_id_local=book_id).first()
    if book:
        # build connection with ebay
        # make request body to ebay
        # execute request to ebay and get response
        ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
        request_info = {
            "Item": {
                "Title": book.title + " " + book.book_id_local,
                "PictureDetails": {
                    # This URL shold be replaced by Allen after finishing S3 storage
                    "PictureURL": book.cover,
                },

                "PrimaryCategory": {
                    "CategoryID": "2228",
                },

                "Country": "AU",
                "Location": book.opshop.opshop_address,
                "Site": "Australia",
                "ConditionID": book.condition,
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": book.opshop.opshop_ebay_email,
                "Description": book.description,
                "ListingDuration": "Days_30",
                "StartPrice": book.price,
                "ListingType": "FixedPriceItem",
                "Currency": "AUD",
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "ShippingDetails": {
                    "ShippingServiceOptions": {
                        "FreeShipping": "True",
                        "ShippingService": "AU_Express"
                    }
                },
                "DispatchTimeMax": "3"
            },
        }
        ebay_conn.execute("AddItem", request_info)
        book.status = 'listed'
        db.session.add(book)
        db.session.commit()

    return book


def list3_book(book, image_links, user):
    ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
    request_info = {
        "Item": {
            "Title": book.title + " " + book.id,
            "PictureDetails": {
                # This URL shold be replaced by Allen after finishing S3 storage
                "PictureURL": image_links[0],
            },

            "PrimaryCategory": {
                "CategoryID": "2228",
            },

            "Country": "AU",
            "Location": user.opshop.address,
            "Site": "Australia",
            "ConditionID": book.condition.value,
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": user.opshop.email,
            "Description": book.description,
            "ListingDuration": "Days_30",
            "StartPrice": book.price,
            "ListingType": "FixedPriceItem",
            "Currency": "AUD",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsAccepted",
                "RefundOption": "MoneyBack",
                "ReturnsWithinOption": "Days_30",
                "ShippingCostPaidByOption": "Buyer"
            },
            "ShippingDetails": {
                "ShippingServiceOptions": {
                    "FreeShipping": "True",
                    "ShippingService": "AU_Express"
                }
            },
            "DispatchTimeMax": "3"
        },
    }
    ebay_conn.execute("AddItem", request_info)
    book.status = ItemStatus.LISTED
    # db.session.add(book)
    # db.session.commit()

    # when book null
    return book


def unlist_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        ebay_conn = Connection(config_file=EbayConfig.config_file, domain="api.sandbox.ebay.com", debug=True)
        request_info = {
            "EndingReason": "LostOrBroken",
            "ItemID": book.book_id_ebay
        }
        ebay_conn.execute("EndItem", request_info)
    book = delete_book(book_id)
    return book


def get_all_books(params, user):
    res = Book.query
    d = {'opshop_id': user['opshop_id'], 'status': ItemStatus.LISTED}
    if 'search' not in params:
        for name in params:

            if name == 'isbn':
                if len(params[name]) == 10:
                    d['ISBN_10'] = params['isbn']
                else:
                    d['ISBN_13'] = params['isbn']
            if name == 'title':
                d[name] = params[name]
        res = res.filter_by(**d)
    else:
        query = '{}%'.format(params['search'])
        query1 = res.filter_by(**d).filter(Book.ISBN_10.like(query))
        query2 = res.filter_by(**d).filter(Book.ISBN_13.like(query))
        query3 = res.filter_by(**d).filter(Book.title.like(query))
        res = query1.union(query2, query3)
    return res.all()


def confirm_book(data, images, token):
    payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(id=payload['user_id']).first()
    data['opshop_id'] = user.opshop.id
    # book_id = data['id']
    # temp = book.__dict__
    # data['_sa_instance_state'] = temp['_sa_instance_state']
    # book.__dict__ = data
    book = Book(**data)
    book.condition = ItemCondition[book.condition]
    book.price = float(book.price)
    image_number = 0
    image_links = []
    for x in images:  # getting images
        image_number = image_number + 1
        image = images[x]
        image.save(str(image_number) + '.png')
        body = open(str(image_number) + '.png', 'rb')
        key = str(data['id']) + '/' + str(image_number) + '.png'

        upload_to_s3(body, key)
        body.close()
        file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)
        image_links.append(file_url)

    book = list3_book(book, image_links, user)
    if book:

        db.session.add(book)
        db.session.commit()

        for i, x in enumerate(image_links):  # getting images
            image_dict = {}  # dictionary analogues to Image object
            if i == 0:  # saving the 1st image returned as cover and updating that in the database
                bookobject = Book.query.filter_by(id=book.id).first()
                bookobject.cover = x
                db.session.commit()

            image_dict['item_id'] = data['id']
            image_dict['aws_link'] = x
            image_object = Image(**image_dict)
            db.session.add(image_object)
            db.session.commit()

    return book
