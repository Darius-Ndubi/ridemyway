import psycopg2

"""
    Method to connect to apps database
"""
def connDb():
    connectdb = "dbname='ridemyway' host='localhost' user='dario' password='riot'"

    #try to connect to database
    try:
        return psycopg2.connect(connectdb)
    except:
        print ("Can't connect to database")


"""
    Method to connect to test database
"""
def connTDb():
    connectdb = "dbname='testride' host='localhost' user='dario' password='riot'"

    #try to connect to database
    try:
        return psycopg2.connect(connectdb)
    except:
        print ("Can't connect to test database")


"""
    Method to destroy the test database after testing
"""
def dropTdb():

    connection=connTDb()
    curs.connection.cursor()
    """DROP TABLE new_user"""
    """DROP TABLE ride"""
    """DROP TABLE requestss"""
    curs.close()
    connection.commit()
    connection.close()

