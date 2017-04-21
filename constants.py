import peewee

DB_HOST = "127.6.156.130"
DB_PORT = 3306
DB_USER = 'adminXSQ1iLK'
DB_PASS = 'e7-fCt_F9UZ3'
DB_DATABASE = 'results'

DB_DEBUG_HOST = "localhost"
DB_DEBUG_PORT = 3306
DB_DEBUG_USER = 'root'
DB_DEBUG_PASS = 'root'
DB_DEBUG_DATABASES = ['results_db', 'results_db_arch']

# db = peewee.MySQLDatabase(DB_DEBUG_DATABASES[0],
#                           host=DB_DEBUG_HOST, port=DB_DEBUG_PORT, user=DB_DEBUG_USER, passwd=DB_DEBUG_PASS)
db = peewee.MySQLDatabase(DB_DATABASE,
                        host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS)


def select_database(database):
    global db
    db = peewee.MySQLDatabase(database,
                              host=DB_DEBUG_HOST, port=DB_DEBUG_PORT, user=DB_DEBUG_USER, passwd=DB_DEBUG_PASS)
