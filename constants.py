import os
import peewee

DB_HOST = os.environ.get('OPENSHIFT_MYSQL_DB_HOST', 'localhost')
DB_PORT = os.environ.get('OPENSHIFT_MYSQL_DB_POORT', 3306)
DB_USER = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', 'root')
DB_PASS = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD', 'trymiracle')

DB_DEBUG_HOST = "localhost"
DB_DEBUG_PORT = 3306
DB_DEBUG_USER = 'root'
DB_DEBUG_PASS = 'root'
DB_DEBUG_DATABASES = ['results_db', 'results_db_arch']

db = peewee.MySQLDatabase(DB_DEBUG_DATABASES[0],
                          host=DB_DEBUG_HOST, port=DB_DEBUG_PORT, user=DB_DEBUG_USER, passwd=DB_DEBUG_PASS)


def select_database(database):
    global db
    db = peewee.MySQLDatabase(database,
                              host=DB_DEBUG_HOST, port=DB_DEBUG_PORT, user=DB_DEBUG_USER, passwd=DB_DEBUG_PASS)
