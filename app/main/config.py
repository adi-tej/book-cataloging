import os

"""
    DB Connection URl
    To connect to local db replace below local_db with your own db url
"""

local_db = 'mysql+pymysql://root:Asdfghjkl834966827@127.0.0.1/circex-dev'
mysql_aws_db = 'mysql+pymysql://circex:CircEx2020@opshops.ch3sf71im1th.ap-southeast-2.rds.amazonaws.com:3306/opshopdb'
basedir = os.path.abspath(os.path.dirname(__file__))

ebay_config_file_path = os.path.abspath("./ebay_config.yaml")


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    DEBUG = False

    """
        AWS S3 Configuration
    """
    S3_BUCKET = 'circexunsw'
    S3_KEY = 'AKIA5WMHZHLO4GDCKDO6'
    S3_SECRET = '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'
    S3_LOCATION = 'https://{}.s3-ap-southeast-2.amazonaws.com'.format(S3_BUCKET)

    """
        Google API Configuration
    """
    GOOGLE_API_KEY = 'AIzaSyBrePeXhgcgWvfEsXPXSsbYGcHEfp0bxAk'
    GOOGLE_API_BASE_URL = 'https://www.googleapis.com'
    GOOGLE_API_BOOK_URL = GOOGLE_API_BASE_URL + '/books/v1/volumes'

    """
        ISBN DB Configuration (it is the circex account(pro version))
    """
    ISBN_BOOK_URL = 'https://api2.isbndb.com/book'
    ISBN_AUTH_KEY = '44506_a940dba3091f4fe691e9c45312d9d919'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = mysql_aws_db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_MASK_SWAGGER = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = mysql_aws_db
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTPLUS_MASK_SWAGGER = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = mysql_aws_db
    RESTPLUS_MASK_SWAGGER = False


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY


class EbayConfig:
    """
        Ebay Configuration
    """
    config_file = ebay_config_file_path
    domain = "api.ebay.com"
    debug = True
