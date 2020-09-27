from ebaysdk.trading import Connection
import os
import requests
from uuid import uuid1, uuid4
import shutil
import boto3
from botocore.client import Config as BotoConfig
from sqlalchemy import desc
import requests
from bs4 import BeautifulSoup

from app.main.model.models import Image, Book, ItemStatus, ItemCondition
from app.main.model.user import User
from .. import db
from app.main.config import EbayConfig
from ..config import Config
import mimetypes
import re

def retrieve_book(data):
	""" Get book info using ISBN from google or ISBN """
	book_data = find_book_info(data)
	if book_data:
		book_data['id'] = uuid1()  # use user id to save image temporarily
		if 'cover' in book_data:
			if book_data['cover']:
				image_r = requests.get(book_data['cover'], stream=True)
				if image_r.status_code == 200:  # if image retrieved succesfully
					# Set decode_content value to True, otherwise the downloaded image file's size will be zero.

					content_type = image_r.headers['content-type']
					extension = mimetypes.guess_extension(content_type)
					file_name = 'example' + str(extension)

					# Open a local file with wb ( write binary ) permission.
					with open(file_name, 'wb') as new_file:
						shutil.copyfileobj(image_r.raw, new_file)

					bookcover = open(file_name, 'rb')  # opening the saved image
					key = str(book_data['id']) + '/' + str(uuid1()) + str(extension)
					upload_to_s3(bookcover, key)  # image saved to amazon s3
					bookcover.close()
					file_url = Config.S3_LOCATION + '/%s' % (key)
					book_data['cover'] = file_url
					new_file.close()
					os.remove(file_name)

	if book_data['cover']:
		book_data['images'] = [{'id': 1, 'uri': book_data['cover']}]
	return book_data


def create_book(data, files, user):
	""" Add new book and list on ebay """
	user = User.query.filter_by(id=user['id']).first()
	data['opshop_id'] = user.opshop.id

	if 'isbn' in data:
		if len(data['isbn']) == 10:
			data['ISBN_10'] = data['isbn']
		else:
			data['ISBN_13'] = data['isbn']
		del data['isbn']
	if 'images' in data:
		del data['images']

	book = Book(**data)
	book.condition = ItemCondition(int(book.condition))

	image_links = []
	if not book.cover:
		delete_from_s3(book.id)
	else:
		image_links.append(book.cover)

	for x in files:  # getting images
		image_key = uuid4()
		file = files[x]
		if file.mimetype == 'image/jpeg':
			filename = str(image_key) + '.png'
			file.save(filename)
			body = open(filename, 'rb')
			key = str(book.id) + '/' + filename

			upload_to_s3(body, key)
			body.close()
			os.remove(filename)
			file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % key
			image_links.append(file_url)

	if image_links and not book.cover:
		book.cover = image_links[0]

	ebay_id = list_book(book, image_links, user)
	book.book_id_ebay = ebay_id
	book.status = ItemStatus.LISTED
	book.item_type_id = 1
	try:
		db.session.add(book)
		db.session.commit()
	except Exception as e:
		print(e)
		db.session.rollback()
		try:
			ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
			request_info = {
				"EndingReason": "LostOrBroken",
				"ItemID": ebay_id
			}
			ebay_conn.execute("EndItem", request_info)
		except Exception as e:
			print(e)
		return None

	for i, x in enumerate(image_links):  # getting images
		image = Image()
		image.uri = x
		image.item_id = book.id
		db.session.add(image)
	db.session.commit()

	return book


def get_book(book_id):
	book = Book.query.filter_by(id=book_id).first()
	return book


def get_all_books(params, user):
	""" Get all listed books by optional title/isbn """
	res = Book.query
	d = {'opshop_id': user['opshop_id'], 'status': ItemStatus.LISTED}
	if 'search' not in params:
		if 'isbn' in params:
			if len(params['isbn']) == 10:
				d['ISBN_10'] = params['isbn']
			else:
				d['ISBN_13'] = params['isbn']
		if 'title' in params:
			query = '{}%'.format(params['title'])
			res = res.filter_by(**d).filter(Book.title.like(query))
		else:
			res = res.filter_by(**d)
	else:
		query = '{}%'.format(params['search'])
		query1 = res.filter_by(**d).filter(Book.ISBN_10.like(query))
		query2 = res.filter_by(**d).filter(Book.ISBN_13.like(query))
		query3 = res.filter_by(**d).filter(Book.title.like(query))
		res = query1.union(query2, query3)
	books = res.order_by(desc(Book.updated_date)).all()
	for book in books:
		book.__dict__['isbn'] = book.ISBN_10 if book.ISBN_10 else book.ISBN_13
	return books


def update_book(data, files, book_id):
	""" Update listed book on ebay """
	if 'isbn' in data:
		if len(data['isbn']) == 10:
			data['ISBN_10'] = data['isbn']
		else:
			data['ISBN_13'] = data['isbn']
		del data['isbn']
	images_str = data['images']
	del data['images']
	book = Book.query.filter_by(id=book_id).first()  # fetching saved book info from table
	for key, value in data.items():
		if data[key]:
			if key == 'id':
				continue
			if key == 'condition':
				book.condition = ItemCondition(int(value))
			elif key == 'price':
				book.price = float(value)
			elif key == 'page_count':
				book.page_count = int(value)
			else:
				setattr(book, key, value)

	image_number = 0
	image_links = []

	for x in files:  # getting images

		image_number = image_number + 1
		file = files[x]
		if file.mimetype == 'image/jpeg':
			file.save(str(image_number) + '.png')
			body = open(str(image_number) + '.png', 'rb')
			key = str(book_id) + '/' + str(image_number) + '.png'

			upload_to_s3(body, key)
			body.close()
			file_url = 'https://circexunsw.s3-ap-southeast-2.amazonaws.com/%s' % (key)
			image_links.append(file_url)

	if image_links and not book.cover:
		book.cover = image_links[0]
	try:
		revise_list_book(book, image_links)
	except Exception:
		pass

	db.session.add(book)
	db.session.commit()
	for i, x in enumerate(image_links):  # getting images
		image = Image()
		image.uri = x
		image.item_id = book.id
		db.session.add(image)

	db.session.commit()

	return book


def delete_book(book_id):
	book = Book.query.filter_by(id=book_id).first()
	if book:
		book.status = ItemStatus.INACTIVE
		db.session.commit()

	return book


'''
    Google API and ISBN DB operations
'''


def find_book_info(isbn):
	book_info = extract_data_google_api(isbn)
	if not book_info:
		book_info = extract_isbndb_api(isbn)
	if book_info == 0:
		return {}  # book info not found in both api,return empty dictionary
	return book_info


def extract_data_google_api(isbn):
	""" Extract book data using google API """
	google_url_book = Config.GOOGLE_API_BOOK_URL + "?q=isbn:{}&key={}".format(isbn,
																			  Config.GOOGLE_API_KEY)  # 9781925483598
	response = requests.get(google_url_book)
	data = response.json()
	book_data = {"isbn": isbn}
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
	return book_data  # return book object


def extract_isbndb_api(isbn):
	""" Extract book data using ISBN DB API """
	isbn_url_book = Config.ISBN_BOOK_URL + "/{}".format(isbn)
	response = requests.get(isbn_url_book, headers={'Authorization': Config.ISBN_AUTH_KEY})
	data = response.json()
	book = data.get("book")
	book_data = {"isbn": isbn}
	if book:
		book_data['title'] = book.get('title', None)
		book_data['author'] = book.get('authors', [None])[0]
		book_data['publisher'] = book.get('publisher', None)
		book_data['page_count'] = book.get('pages', None)
		book_data['cover'] = book.get('image', None)

	return book_data


'''
    Ebay API operations
'''


def list_book(book, image_links, user):
	"""this function lists the book to ebay """
	ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
	request_info = {
		"Item": {
			"Title": book.title + " " + book.id,
			"PictureDetails": {
				# This URL shold be replaced by Allen after finishing S3 storage
				"PictureURL": image_links
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


def revise_list_book(book, images):
	""" Update book listing in ebay """
	ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
	request_info = {
		"Item": {
			"ItemID": book.book_id_ebay,
			"Title": book.title + " " + book.id,
			"PictureDetails": {
				"PictureURL": images,

				# -- more PictureURL values are allowed here -- #
			},
			"ConditionID": book.condition.value,
			"Description": book.description,
			"StartPrice": book.price

		}
	}

	ebay_conn.execute("ReviseItem", request_info)

	return


def unlist_book(book_id):
	""" Unlist book from ebay """
	book = Book.query.filter_by(id=book_id).first()
	try:
		ebay_conn = Connection(config_file=EbayConfig.config_file, domain=EbayConfig.domain, debug=EbayConfig.debug)
		request_info = {
			"EndingReason": "LostOrBroken",
			"ItemID": book.book_id_ebay
		}
		ebay_conn.execute("EndItem", request_info)
	except Exception:
		pass
	book.status = ItemStatus.INACTIVE
	db.session.add(book)
	db.session.commit()
	return book


'''
	AWS S3 Operations
'''


def s3_bucket():
	return boto3.resource(
		's3',
		aws_access_key_id=Config.S3_KEY,
		aws_secret_access_key=Config.S3_SECRET,
		config=BotoConfig(signature_version='s3v4')
	).Bucket(Config.S3_BUCKET)


def delete_from_s3(key):
	s3 = s3_bucket()
	for obj in s3.objects.filter(Prefix=key + '/'):
		obj.delete()


def upload_to_s3(body, name):
	s3 = s3_bucket()
	s3.put_object(Key=name, Body=body)


def auto_price(isbn):
	url = 'https://www.ebay.com.au/sch/i.html?_from=R40&_nkw=%{isbn}&_sacat=0&_sop=15'
	url = url.format(isbn=isbn)

	html = requests.get(url)

	soup = BeautifulSoup(
		html.text,
		'html.parser'
	)

	results = soup.find_all('div', attrs={'class': 's-item__info clearfix'})

	price_array = []

    i = 0
    for item in results:
        if i < 10:
            price_info = {}

            inside = item.find_all('div', attrs={'class': 's-item__details clearfix'})
            inside_tag = inside[0]
            price_tags = inside_tag.find_all('div', attrs={'class': 's-item__detail s-item__detail--primary'})
            country_tag = inside_tag.find('span', attrs={'class': 's-item__detail s-item__detail--secondary'})

            if price_tags[0].find('span', attrs={'class': 's-item__price'}):
                price_info['item_price'] = price_tags[0].find('span', attrs={'class': 's-item__price'}).text.split()[1]

                pat = re.compile(r'^\$\s*([0-9.]*)')
                if pat.match(price_info['item_price']):
                    price_info['item_price'] = float(pat.match(price_info['item_price']).group(1))
            else:
                price_info['item_price'] = 0

            if price_tags[2].find('span', attrs={'class': 's-item__shipping s-item__logisticsCost'}):
                price_info['logistics_price'] = \
                    price_tags[2].find('span', attrs={'class': 's-item__shipping s-item__logisticsCost'}).text.split()[1]

                pat = re.compile(r'^\$\s*([0-9.]*)')
                if pat.match(price_info['logistics_price']):
                    price_info['logistics_price'] = float(pat.match(price_info['logistics_price']).group(1))

                if price_info['logistics_price'] == "postage":
                    price_info['logistics_price'] = 0
            else:
                price_info['logistics_price'] = 0

            if country_tag:
                country = country_tag.find('span', attrs={'class': 's-item__location s-item__itemLocation'})
                if country:
                    price_info['item_location'] = country.text

                    # remove "from" at the beginning
                    pattern = re.compile(r'From\s*(.*)', re.I)
                    if pattern.match(price_info['item_location']):
                        price_info['item_location'] = pattern.match(price_info['item_location']).group(1)
                else:
                    price_info['item_location'] = 'Australia'
            price_array.append(price_info)
            i += 1

	return price_array
