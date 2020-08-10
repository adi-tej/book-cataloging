import os

# circex:CircEx2020@opshops.ch3sf71im1th.ap-southeast-2.rds.amazonaws.com:3306/opshopdb
mysql_aws_db = 'mysql+pymysql://circex:CircEx2020@opshops.ch3sf71im1th.ap-southeast-2.rds.amazonaws.com:3306/opshopdb'

basedir = os.path.abspath(os.path.dirname(__file__))

ebay_config_file_path = os.path.abspath("./ebay_config.yaml")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_secret_key')
    DEBUG = False

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
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

class EbayConfig:
    config_file = ebay_config_file_path
    domain = "api.ebay.com"
    debug = True