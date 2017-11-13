import mysql.connector
from mysql.connector import errorcode


class UseDatabase:

    def __init__(self, dbconfig : dict):
        self.dbconfig = dbconfig

    def __enter__(self):
        try:
            self.cnx = mysql.connector.connect(**self.dbconfig)
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()

