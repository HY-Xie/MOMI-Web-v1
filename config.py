#encoding: utf-8
import os

# for debug use only
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0

port = 9090

SECRET_KEY = os.urandom(24)

# database
DIALECT = "mysql"
DRIVER = "pymysql"
HOST = "127.0.0.1"
PORT = "3306"
USERNAME = "root"
PASSWORD = "."
DATABASE = "miomi_web"
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
DB_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


SQLALCHEMY_TRACK_MODIFICATIONS = False