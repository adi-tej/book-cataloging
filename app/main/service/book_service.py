from flask import jsonify, make_response
from datetime import datetime
from ebaysdk.trading import Connection
import json
import requests
from uuid import uuid1
import shutil
import boto3
from botocore.client import Config as BotoConfig
from app.main.model.models import Image, Book, ItemStatus, ItemCondition
from app.main.model.user import User
from ..util.decorator import TOKEN
from .. import db
from app.main.config import EbayConfig
from ..config import Config


def find_book_info(isbn):  # function to search book in both api
    book_info = extract_data_google_api(isbn)
    if not book_info:
        book_info = extract_isbndb_api(isbn)
    if book_info == 0:
        return {}  # book info not found in both api,return empty dictionary

    return book_info


def extract_data_google_api(isbn):
    google_url_book = Config.GOOGLE_API_BOOK_URL + "?q=isbn:{}&key={}".format(isbn,
                                                                              Config.GOOGLE_API_KEY)  # 9781925483598
    response = requests.get(google_url_book)
    data = response.json()
    book_data = {}  # empty dictionary

    if data['totalItems'] == 0:
        return None  # return None when item not found

    book = data['items'][0].get('volumeInfo', None)
    if book:
        book_data['title'] = book.get('title', None)
        book_data['author'] = book.get('authors', [None])[0]
        book_data['genre'] = book.get('categories', [None])[0]
        book_data["publisher"] = book.get('publisher', None)
        # book_data["publish_date"] = book.get('publishedDate', None)
        book_data["page_count"] = book.get('pageCount', None)
        book_data["description"] = book.get('description', None)
        book_data['cover'] = book.get('imageLinks', {}).get('thumbnail', None)
        book_data["isbn"] = book.get('industryIdentifiers', [0, {}])[1].get('identifier', None)
        if not book_data["isbn"]:
            book_data["isbn"] = book.get('industryIdentifiers', [{}])[0].get('identifier', None)
    return book_data  # return book object


def extract_isbndb_api(isbn):
    isbn_url_book = Config.ISBN_BOOK_URL + "/{}".format(isbn)
    response = requests.get(isbn_url_book, headers={'Authorization': Config.ISBN_AUTH_KEY})
    data = response.json()
    # parsed = json.loads(data)
    # print("parsed in function ISBNDB ", parsed)
    book = data.get("book")

    book_data = {}  # empty dictionary
    if book:
        book_data['title'] = book.get('title', None)
        book_data['author'] = book.get('authors', [None])[0]
        book_data['publisher'] = book.get('publisher', None)
        book_data['page_count'] = book.get('pages', None)
        book_data['cover'] = book.get('image', None)
        book_data['isbn'] = book.get('isbn', book.get('isbn13', None))

    return book_data


def upload_to_s3(body, name):
    # ACCESS_KEY_ID = 'AKIA5WMHZHLO4GDCKDO6'
    # ACCESS_SECRET_KEY = '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'
    # BUCKET_NAME = 'circexunsw'
    s3 = boto3.resource(
        's3',
        aws_access_key_id=Config.S3_KEY,
        aws_secret_access_key=Config.S3_SECRET,
        config=BotoConfig(signature_version='s3v4')
    )
    # image upload
    s3.Bucket(Config.S3_BUCKET).put_object(Key=name, Body=body)


def retrieve_book(data):

    book_data = find_book_info(data)

    if book_data:
        book_data['id'] = uuid1()  # use user id to save image temporarily
        # book_data['book_id_ebay'] = ''

        if book_data['cover']:
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
                file_url = Config.S3_LOCATION+'/%s' % (key)
                book_data['cover'] = file_url  ## amazon url of file overwritten in Book['cover']
                new_file.close()
                # os.remove(file_name)
                # print("Attachment Successfully save in S3 Bucket url %s " % (file_url))

    # book = Book()
    #
    # book.__dict__ = book_data
    if book_data['cover']:
        book_data['images'] = [{'id':0,'uri':book_data['cover']}]
    return book_data


def revise_list_book(book):
    ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
    request_info = {
        "Item": {
            "ItemID":book.book_id_ebay,
            "PictureDetails": {
                "PictureURL": "URL-1",
                "PictureURL": "URL-2",
                # -- more PictureURL values are allowed here -- #
            },
        }
    }
    ebay_conn.execute("ReviseItem", request_info)


def update_book(data, images, book_id):

    book = Book.query.filter_by(id=book_id).first()  # fetching saved book info from table

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
            # if image_number == 1:  # updating  the new  1st image as cover
            #     book.cover = file_url
            image_object = Image()
            image_dict['item_id'] = book.id
            image_dict['aws_link'] = file_url
            temp = image_object.__dict__
            # image_dict['_sa_instance_state'] = temp['_sa_instance_state']
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
        book.status = ItemStatus.INACTIVE
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
    resp = ebay_conn.execute("AddItem", request_info)
    return resp.dict()["ItemID"]
    # db.session.add(book)
    # db.session.commit()

    # when book null
    # return book


def unlist_book(book_id):

    book = Book.query.filter_by(id=book_id).first()
    if book:
        try:
            ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
            request_info = {
                "EndingReason": "LostOrBroken",
                "ItemID": book.book_id_ebay
            }
            ebay_conn.execute("EndItem", request_info)
        except:
            pass

        book.status = ItemStatus.INACTIVE
        db.session.add(book)
        db.session.commit()
        # book = delete_book(book_id)
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
    books = res.all()
    for book in books:
        book.__dict__['isbn'] = book.ISBN_10 if book.ISBN_10 else book.ISBN_13
    return books


def confirm_book(data, images, user):
    # payload = TOKEN.serializer.loads(token.encode())
    user = User.query.filter_by(id=user['id']).first()
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

    ebay_id = list3_book(book, image_links, user)
    book.book_id_ebay = ebay_id
    book.status = ItemStatus.LISTED
    book.cover = image_links[0]
    db.session.add(book)
    db.session.commit()
    for i, x in enumerate(image_links):  # getting images
        image_dict = {'item_id': data['id'], 'uri': x}
        image_object = Image(**image_dict)
        db.session.add(image_object)
    db.session.commit()

    return book
