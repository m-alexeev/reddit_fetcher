import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os

load_dotenv()


USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
DATABASE = os.getenv("DB")
URL = os.getenv("DB_URL")

class Database:
    connection = None
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(host = URL,
                                                user = USERNAME, 
                                                password = PASSWORD,
                                                database = DATABASE)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCES_DENIED_ERROR:
                print("Invalid Credentials")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)


    def getConnection(self):
        return self.connection