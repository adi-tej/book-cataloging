from flask import jsonify, make_response
from datetime import datetime
from ebaysdk.trading import Connection

from ..http_status import *

def find_book_info(ISBN):  # function to search book in both api
    book_info = extract_data_google_api(ISBN)
    if book_info == 0:
        book_info = extract_isbndb_api(ISBN)
    if book_info == 0:
        return {}  # book info not found in both api,return empty dictionary

    return book_info


def extract_data_google_api(ISBN):
    API_KEY = "AIzaSyD6-khCY5wCvJbq0JYCIyw75gfxTtgHt_o"  # google api key
    google_url_book = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}&key={}".format(ISBN,
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
    except KeyError:
        book_data['title'] = "NA"
    try:
        book_data['author'] = book_info['volumeInfo']['authors'][0]
    except KeyError:
        book_data['author'] = "NA"
    try:
        book_data['genre'] = book_info['volumeInfo']['categories'][0]
    except KeyError:
        book_data['genre'] = "NA"
    try:
        book_data["publisher"] = book_info['volumeInfo']['publisher']
    except KeyError:
        book_data["publisher"] = "NA"
    try:
        book_data["publish_date"] = book_info['volumeInfo']['publishedDate']
    except KeyError:
        book_data["publish_date"] = "NA"
    try:
        book_data["pages_number"] = book_info['volumeInfo']['pageCount']
    except KeyError:
        book_data["pages_number"] = "NA"
    try:
        book_data["description"] = book_info['volumeInfo']['description']
    except KeyError:
        book_data["description"] = "NA"
    try:
        book_data['cover'] = book_info['volumeInfo']['imageLinks']['thumbnail']
    except KeyError:
        book_data['cover'] = "NA"
    try:
        book_data["ISBN_10"] = book_info['volumeInfo']['industryIdentifiers'][0]['identifier']
    except KeyError:
        book_data['ISBN_10'] = "NA"
    try:
        book_data["ISBN_13"] = book_info['volumeInfo']["industryIdentifiers"][1]['identifier']
    except KeyError:
        book_data["ISBN_13"] = "NA"

    return book_data  # return book object


def extract_isbndb_api(ISBN):
    isbn_url_book = "https://api2.isbndb.com/book/{}".format(ISBN)
    h = {'Authorization': '44245_0eebc755e9df899dbcdd5121c6cca21f'}
    response = requests.get(isbn_url_book, headers=h)
    data = response.text
    parsed = json.loads(data)
    print("parsed in function ", parsed)
    book_info = parsed.get("book")

    book_data = {}  # empty dictionary
    if book_info:

        try:
            book_data['title'] = book_info['title']
        except KeyError:
            book_data["title"] = "NA"
        try:
            book_data['author'] = book_info['authors'][0]
        except KeyError:
            book_data["author"] = "NA"
        try:
            book_data["publisher"] = book_info['publisher']
        except KeyError:
            book_data['publisher'] = "NA"
        try:
            book_data["publish_date"] = book_info["publish_date"]
        except KeyError:
            book_data["publish_date"] = "NA"
        try:
            book_data["pages_number"] = book_info['pages']
        except KeyError:
            book_data["pages_number"] = "NA"
        try:
            book_data['cover'] = book_info['image']
        except KeyError:
            book_data['cover'] = "NA"
        try:
            book_data["ISBN_10"] = book_info["isbn"]
        except KeyError:
            book_data["ISBN_10"] = 'NA'
        try:
            book_data["ISBN_13"] = book_info["isbn13"]
        except KeyError:
            book_data['ISBN_13'] = "NA"

        return book_data

    else:

        return 0  # return 0 when item not found

def upload_to_s3(body,name):

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
    book = Book()

    book_data = find_book_info(data["ISBN"])

    book_data['book_id_local'] = book_id_local = uuid5(NAMESPACE_OID, 'v5app')
    book_data['book_id_ebay'] = ''
    book_data['item_type_id'] = 1
    book_data['create_date'] = datetime.now()
    book_data['update_date'] = datetime.now()
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
            key = str(book_data['book_id_local']) + '/cover.png'
            upload_to_s3(bookcover, key)  # image saved to amazon s3
            bookcover.close()
            file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)
            book_data['cover1'] = file_url  ## amazon url of file overwritten in Book['cover']
            new_file.close()
            # os.remove(file_name)
            # print("Attachment Successfully save in S3 Bucket url %s " % (file_url))

    except KeyError:
        pass

    book.__dict__ = book_data

    db.session.add(book)
    db.session.commit()

    resp = make_response(jsonify(book.__dict__))
    resp.status_code = POST_SUCCESS
    resp.headers['message'] = 'add book success'

    return resp

def update_book(data, book_id):
    book = Book.query.filter_by(book_id_loacl=book_id).first()  # fetching saved book info from table
    book_data = book.__dict__

    for key in new_data:
        book_data[key] = data[key]  # updating new info

    image_number = 0
    for x in request.files:
        image_number = image_number + 1
        image = request.files[x]
        image.save(str(image_number) + '.png')
        body = open(str(image_number) + '.png', 'rb')
        key = str(data['book_id_local']) + '/' + str(image_number) + '.png'

        upload_to_s3(body, key)
        body.close()
        file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)
        book_data['cover' + str(image_number)] = file_url

    book.__dict__ = book_data
    db.session.add(book)
    db.session.commit()

    resp = make_response(jsonify(book.__dict__))
    resp.status_code = POST_SUCCESS

    return resp

def get_book(book_id):
    book = Book.query.filter_by(book_id_loacl=book_id).first()
    if not book:
        resp = make_response(jsonify({'message':'book not found'}))
        resp.status_code = NOT_FOUND
        return resp
    else:
        book_info = json.dumps(book.__dict__)
        resp = make_response(jsonify(book_info))
        resp.status_code = GET_SUCCESS
        return resp

def delete_book(book_id):
    book = Book.query.filter_by(book_id_loacl=book_id).first()
    if not book:
        resp = make_response(jsonify({'message': 'book not found'}))
        resp.status_code = NOT_FOUND
        return resp
    else:
        resp = make_response(jsonify(book.__dict__))
        db.session.remove(book)
        db.session.commit()
        resp.status_code = GET_SUCCESS
        return resp

def list_book(data):
    fail_list = []
    if data['books']:
        for book_id in data['books']:
            book = Book.query.filter_by(book_local_id=book_id).first()
            if not book:
                fail_list.append(book_id)
            else:
                # build connection with ebay
                # make request body to ebay
                # execute request to ebay and get response
                ebay_conn = Connection(config_file="ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
                request_info = {
                    "Item": {
                        "Title": book.title + " " + book.book_id_local,
                        "PictureDetails": {
                            # This URL shold be replaced by Allen after finishing S3 storage
                            "PictureURL": book.cover1,
                        },
                        "Country": "AU",
                        "Location": book.opshop.opshop_address,
                        "Site": "Australia",
                        "SiteID": 15,
                        "ConditionID": book.condition_id,
                        "PaymentMethods": "PayPal",
                        "PayPalEmailAddress": book.opshop.opshop_ebay_email,
                        "Description": book.description,
                        "ListingDuration": "Days_30",
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
                                "ShippingService": "ShippingMethodStandard"
                            }
                        },
                        "DispatchTimeMax": "3"
                    },
                }
                response_ebay = ebay_conn.execute("AddItem", request_info)
                # book list failed
                if not response_ebay['Category2ID']:
                    fail_list.append(book_id)
                else:
                    book.__dict__['status'] = 'listed'
                    book.__dict__['book_id_ebay'] = response_ebay['ItemID']
                    db.session.add(book)
                    db.session.commit()

        if fail_list:
            fail_dict = {
                'failed':fail_list,
                'operation':'list',
                'message':'some items list failed'
            }
            resp = make_response(jsonify(fail_dict))
            resp.status_code = BAD_REQUEST
            return resp
        else:
            resp = make_response(jsonify({'message':'all items list success'}))
            resp.status_code = POST_SUCCESS
            return resp
    else:
        resp = make_response(jsonify({'message':'no book found'}))
        resp.status_code = BAD_REQUEST
        return resp

def unlist_book(data):
    fail_unlist = []
    if data['books']:
        for book_id in data['books']:
            book = Book.query.filter_by(book_local_id=book_id).first()
            if not book:
                fail_unlist.append(book_id)
            else:
                ebay_conn = Connection(config_file="ebay_config.yaml", domain="api.sandbox.ebay.com", debug=True)
                request_info = {
                    "EndingReason": "LostOrBroken",
                    "ItemID": book.book_id_ebay
                }
                response_ebay = ebay_conn.execute("EndItem", request_info)
        if fail_unlist:
            fail_dict = {'failed': fail_unlist, 'operation': 'unlist'}
            resp = make_response(jsonify(fail_dict))
            resp.status_code = BAD_REQUEST
            resp.headers['message'] = 'some items unlist failed'
            return resp
        else:
            resp = make_response()
            resp.status_code = POST_SUCCESS
            resp.headers['message'] = 'all items unlist success'
            return resp
    else:
        resp = make_response(jsonify({'message':'no book found'}))
        resp.status_code = BAD_REQUEST
        return resp