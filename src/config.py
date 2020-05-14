from os import path

# GENERAL SETTINGS --------------------------------------------
# Getting the parent directory of this file. That will function as the project home.
PROJECT_HOME = path.dirname(path.dirname(path.abspath(__file__)))

# LOGGING SETTINGS --------------------------------------------
# specify logging configuration file location
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

# RAW DATA SETTINGS ------------------------------------------
# URL from which to download data
RAW_DATA_LOCATION = "https://data.cityofchicago.org/api/views/mft5-nfa8/rows.csv?accessType=DOWNLOAD"

# S3 SETTINGS ------------------------------------------------
# S3 bucket into which data will be placed (user must have WRITE privileges)
S3_BUCKET_NAME = "merrell-copa-cases"
# S3 key name to use when uploading data
S3_KEY_NAME = "copa_raw_data"

# DATABASE SETTINGS ------------------------------------------
# Local SQLite setup
DATABASE_PATH = path.join(PROJECT_HOME, 'data/copa.db')
LOCAL_URI = 'sqlite:////{}'.format(DATABASE_PATH)

#RDS instance setup
MYSQL_CONN_TYPE = "mysql+pymysql"
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")
RDS_URI = "{}://{}:{}@{}:{}/DATABASE_NAME".format(MYSQL_CONN_TYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT)

# Input desired type (Local vs. RDS) below
SQLALCHEMY_DATABASE_URI = RDS_URI
